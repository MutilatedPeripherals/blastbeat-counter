# Blast beat counter

## MVP Roadmap

- [X] Identify frequencies of snare & bass drum (hihat left for next iteration)
    - snare: 300hz
    - bass drum: 50hz
- [X] Process the waveform (0.5s segments) and determine: 1) does it contain snare, 2) does it contain bass drum
- [X] If at least 4 consecutive segments contain snare + bass drum, count it as a blast beat
- [X] Plot the waveform with the blast beat segments highlighted
- [ ] Test with other types of blast beats
