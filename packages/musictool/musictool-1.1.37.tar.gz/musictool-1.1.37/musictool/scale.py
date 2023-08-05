from __future__ import annotations

import functools
import itertools
from collections import defaultdict

from musictool import config
from musictool.chord import Chord
from musictool.note import Note
from musictool.noteset import NoteSet
from musictool.piano import Piano
from musictool.util.color import hex_to_rgb


class Scale(NoteSet):
    intervals_to_name = {
        # diatonic
        frozenset({0, 2, 4, 5, 7, 9, 11}): 'major',
        frozenset({0, 2, 3, 5, 7, 9, 10}): 'dorian',
        frozenset({0, 1, 3, 5, 7, 8, 10}): 'phrygian',
        frozenset({0, 2, 4, 6, 7, 9, 11}): 'lydian',
        frozenset({0, 2, 4, 5, 7, 9, 10}): 'mixolydian',
        frozenset({0, 2, 3, 5, 7, 8, 10}): 'minor',
        frozenset({0, 1, 3, 5, 6, 8, 10}): 'locrian',
        # harmonic
        frozenset({0, 2, 3, 5, 7, 8, 11}): 'h_minor',
        frozenset({0, 1, 3, 5, 6, 9, 10}): 'h_locrian',
        frozenset({0, 2, 4, 5, 8, 9, 11}): 'h_major',
        frozenset({0, 2, 3, 6, 7, 9, 10}): 'h_dorian',
        frozenset({0, 1, 4, 5, 7, 8, 10}): 'h_phrygian',
        frozenset({0, 3, 4, 6, 7, 9, 11}): 'h_lydian',
        frozenset({0, 1, 3, 4, 6, 8, 9}): 'h_mixolydian',
        # melodic
        frozenset({0, 2, 3, 5, 7, 9, 11}): 'm_minor',
        frozenset({0, 1, 3, 5, 7, 9, 10}): 'm_locrian',
        frozenset({0, 2, 4, 6, 8, 9, 11}): 'm_major',
        frozenset({0, 2, 4, 6, 7, 9, 10}): 'm_dorian',
        frozenset({0, 2, 4, 5, 7, 8, 10}): 'm_phrygian',
        frozenset({0, 2, 3, 5, 6, 8, 10}): 'm_lydian',
        frozenset({0, 1, 3, 4, 6, 8, 10}): 'm_mixolydian',
        # pentatonic
        frozenset({0, 2, 4, 7, 9}): 'p_major',
        frozenset({0, 2, 5, 7, 10}): 'p_dorian',
        frozenset({0, 3, 5, 8, 10}): 'p_phrygian',
        frozenset({0, 2, 5, 7, 9}): 'p_mixolydian',
        frozenset({0, 3, 5, 7, 10}): 'p_minor',
        # sudu
        frozenset({0, 2, 4, 5, 7, 9}): 's_major',
        frozenset({0, 2, 3, 5, 7, 10}): 's_dorian',
        frozenset({0, 1, 3, 5, 8, 10}): 's_phrygian',
        frozenset({0, 2, 4, 7, 9, 11}): 's_lydian',
        frozenset({0, 2, 5, 7, 9, 10}): 's_mixolydian',
        frozenset({0, 3, 5, 7, 8, 10}): 's_minor',
    }
    name_to_intervals = {v: k for k, v in intervals_to_name.items()}
    root: Note

    def __init__(
        self,
        notes: frozenset[str | Note],
        *,
        root: str | Note,
    ):
        # if not isinstance(root, str | Note):

        super().__init__(notes, root=root)

        if self.name is None:
            raise TypeError('scale is not supported')
        self.kind = config.kinds[self.name]
        scales = getattr(config, self.kind)
        _scale_i = scales.index(self.name)
        scales = scales[_scale_i:] + scales[:_scale_i]
        self.note_scales = {}
        for note, scale in zip(self.notes_ascending, scales, strict=True):
            self.note_scales[note] = scale

        if self.kind == 'diatonic':
            self.triads = self._make_nths(frozenset({0, 2, 4}))
            self.sevenths = self._make_nths(frozenset({0, 2, 4, 6}))
            self.ninths = self._make_nths(frozenset({0, 2, 4, 6, 8}))
            self.notes_to_triad_root = {triad.notes: triad.root for triad in self.triads}
            self.notes_to_seventh_root = {seventh.notes: seventh.root for seventh in self.sevenths}
            self.notes_to_ninth_root = {ninth.notes: ninth.root for ninth in self.ninths}
        self.html_classes += self.name,

    def _make_nths(self, ns: frozenset[int]) -> tuple[Chord, ...]:
        return tuple(
            Chord(frozenset(self.notes_ascending[(i + n) % len(self)] for n in ns), root=self.notes_ascending[i])
            for i in range(len(self))
        )

    def parallel(self, parallel_name: str) -> Scale:
        """same root, changes set of notess"""
        return Scale.from_name(self.root, parallel_name)

    def relative(self, relative_name: str) -> Scale:
        """same set of notes, changes root"""
        for note, name in self.note_scales.items():
            if name == relative_name:
                return Scale.from_name(note, name)
        raise KeyError(f'relative {relative_name} scale not found')

    def to_piano_image(self):
        return Piano(notes=self.notes, note_scales=self.note_scales)._repr_svg_()

    def _repr_html_(self) -> str:
        chords_hover = ''
        if C_name := self.note_scales.get(Note('C'), ''):
            C_name = f' | C {C_name}'
        return f"""
        <div class='{' '.join(self.html_classes)}' {chords_hover}>
        <a href='{self.root.name}'><span class='card_header'><h3>{self.root.name} {self.name}{C_name}</h3></span></a>
        {self.to_piano_image()}
        </div>
        """

# flake8: noqa


class ComparedScales:
    """
    this is compared scale
    local terminology: left scale is compared to right
    left is kinda parent, right is kinda child
    """

    def __init__(self, left: Scale, right: Scale):
        self.left = left
        self.right = right
        self.key = left, right
        self.shared_notes = frozenset(left.notes) & frozenset(right.notes)
        self.new_notes = frozenset(right.notes) - frozenset(left.notes)
        self.del_notes = frozenset(left.notes) - frozenset(right.notes)
        if right.kind == 'diatonic':
            self.shared_triads = frozenset(left.triads) & frozenset(right.triads)
        self.html_classes: tuple[str, ...] = ('card',)

    def with_html_classes(self, classes: tuple[str, ...]) -> str:
        prev = self.html_classes
        self.html_classes = prev + classes
        r = self._repr_html_()
        self.html_classes = prev
        return r

    # def __format__(self, format_spec): raise No

    # @functools.cached_property
    def _repr_html_(self) -> str:
        chords_hover = ''
        if C_name := self.right.note_scales.get(Note('C'), ''):
            C_name = f' | C {C_name}'
        return f"""
        <div class='{' '.join(self.html_classes)}' {chords_hover}>
        <a href='{self.right.root.name}'><span class='card_header'><h3>{self.right.root.name} {self.right.name}{C_name}</h3></span></a>
        {self.to_piano_image()}
        </div>
        """

    def to_piano_image(self):
        return Piano(
            notes=self.right.notes,
            note_scales=self.right.note_scales,
            red_notes=self.del_notes, green_notes=self.new_notes, blue_notes=self.shared_notes,
            notes_squares={
                chord.root: (
                    hex_to_rgb(config.chord_colors[chord.name]),
                    config.BLUE if chord in self.shared_triads else config.BLACK_BRIGHT,
                    config.BLUE if chord in self.shared_triads else config.BLACK_BRIGHT,
                    str(chord),
                )
                for chord in self.right.triads
            } if self.right.kind == 'diatonic' else dict(),
        )._repr_svg_()

    def __eq__(self, other): return self.key == other.key
    def __hash__(self): return hash(self.key)
    def __repr__(self): return f'ComparedScale({self.left.root} {self.left.name} | {self.right.root} {self.right.name})'


diatonic = {(root, name): Scale.from_name(root, name) for root, name in itertools.product(config.chromatic_notes, config.diatonic)}
harmonic = {(root, name): Scale.from_name(root, name) for root, name in itertools.product(config.chromatic_notes, config.harmonic)}
melodic = {(root, name): Scale.from_name(root, name) for root, name in itertools.product(config.chromatic_notes, config.melodic)}
pentatonic = {(root, name): Scale.from_name(root, name) for root, name in itertools.product(config.chromatic_notes, config.pentatonic)}
sudu = {(root, name): Scale.from_name(root, name) for root, name in itertools.product(config.chromatic_notes, config.sudu)}
all_scales = {
    'diatonic': diatonic,
    'harmonic': harmonic,
    'melodic': melodic,
    'pentatonic': pentatonic,
    'sudu': sudu,
}

# circle of fifths clockwise
majors = dict(
    diatonic=tuple(diatonic[note, 'major'] for note in 'CGDAEBfdaebF'),
    harmonic=tuple(harmonic[note, 'h_major'] for note in 'CGDAEBfdaebF'),
    melodic=tuple(melodic[note, 'm_major'] for note in 'CGDAEBfdaebF'),
    pentatonic=tuple(pentatonic[note, 'p_major'] for note in 'CGDAEBfdaebF'),
    sudu=tuple(sudu[note, 's_major'] for note in 'CGDAEBfdaebF'),
)


@functools.cache
def neighbors(left: Scale) -> dict[int, list[ComparedScales]]:
    neighs = defaultdict(list)
    for right_ in all_scales[left.kind].values():
        # if left == right:
        #     continue
        right = ComparedScales(left, right_)
        neighs[len(right.shared_notes)].append(right)
    return neighs
