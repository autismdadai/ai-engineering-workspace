# Trig reference card

Section pointers are to *Trigonometry*, Version 2 (2023), the open textbook from Salt Lake Community College, the University of Utah, Weber State University and Utah Valley University (license CC BY-NC-SA 3.0). Page codes such as T3-19 are the book's own.

## Degrees and radians (§1.1, T1-3)

180° = π radians. To go from degrees to radians, multiply by π/180; from radians to degrees, multiply by 180/π.

## Exact values (§1.3, The Unit Circle, T1-39)

| Angle | 0 | 30° (π/6) | 45° (π/4) | 60° (π/3) | 90° (π/2) |
|---|---|---|---|---|---|
| sin | 0 | 1/2 | √2/2 | √3/2 | 1 |
| cos | 1 | √3/2 | √2/2 | 1/2 | 0 |
| tan | 0 | √3/3 | 1 | √3 | undefined |

Signs by quadrant: everything is positive in quadrant I, only sin in II, only tan in III, only cos in IV.

## Core identities (§1.5, T1-76; §3.1, T3-3; §3.2, T3-19)

- sin²x + cos²x = 1, 1 + tan²x = sec²x, 1 + cot²x = csc²x
- tan x = sin x / cos x
- cos(a ± b) = cos a cos b ∓ sin a sin b
- sin(a ± b) = sin a cos b ± cos a sin b
- sin 2x = 2 sin x cos x
- cos 2x = cos²x − sin²x = 1 − 2 sin²x = 2 cos²x − 1
- sin²x = (1 − cos 2x)/2, cos²x = (1 + cos 2x)/2
- cos(−x) = cos x, sin(−x) = −sin x

## Triangles (§5.1, The Law of Sines, T5-3; §5.2, The Law of Cosines, T5-30)

Label the sides a, b, c and the opposite angles A, B, C.

- Law of sines: a / sin A = b / sin B = c / sin C
- Law of cosines: c² = a² + b² − 2ab cos C
- Area = ½ ab sin C
- Which to use: for SSS or SAS, start with the law of cosines. For ASA or AAS, get the third angle from 180°, then use the law of sines. SSA is the ambiguous case.
- The SSA rule: with A, a and b known, sin B = b sin A / a. Above 1, there's no triangle. Exactly 1, there's one right triangle. Below 1, B can be the acute angle or 180° minus it, and each choice that keeps A + B under 180° gives a triangle, so there can be two.

## Complex numbers and vectors (§6.3, T6-50; §6.4, T6-60; §7.3, T7-32)

- Polar form: a complex number is r(cos θ + i sin θ). Multiplying two of them multiplies the lengths and adds the angles. Euler's formula, e^{iθ} = cos θ + i sin θ, is the same thing written as an exponential.
- Dot product: u · v = |u| |v| cos θ.

This is the trig behind the phases e^{iφ} in quantum states and behind the CHSH correlator −cos(a − b) in the quantum lab skill.
