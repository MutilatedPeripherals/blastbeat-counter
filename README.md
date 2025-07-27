# Blast beat counter

What is a blast beat? This is what wikipedia has to say:
> A blast beat is a type of drum beat that originated in hardcore punk and grindcore, and is often associated with
> certain styles of extreme metal, namely black metal, death metal and their respective subgenres. The blast-beat
> generally comprises a repeated, sixteenth-note figure
> played
> at a very fast tempo, and divided uniformly among the bass drum, snare, and ride, crash, or hi-hat cymbal."

As metal maniacs and programmers, we naturally asked ourselves:
> Can we identify blast beats programmatically?

After isolating the drums and analyzing the spectrogram, we observed a very clear pattern (example song: Dying Fetus -
Subjected to a Beating):
![audacity_analysis.png](output/audacity_analysis.png)

Here is our first result with the current MVP:
![Dying_Fetus___Subjected_To_A_Beating.png](output/Dying_Fetus___Subjected_To_A_Beating.png)

## MVP Roadmap

- [X] Identify frequencies of snare & bass drum (hihat left for next iteration)
    - snare: 300hz
    - bass drum: 50hz
- [X] Process the waveform (0.5s segments) and determine: 1) does it contain snare, 2) does it contain bass drum
- [X] If at least 4 consecutive segments contain snare + bass drum, count it as a blast beat
- [X] Plot the waveform with the blast beat segments highlighted
- [ ] Test with other types of blast beats
