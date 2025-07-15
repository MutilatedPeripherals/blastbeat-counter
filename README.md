# Blast beat counter

![Dying Fetus - Subjected To A Beating.png](output/Dying%20Fetus%20-%20Subjected%20To%20A%20Beating.png)

## Plan

- [X] Identify frequencies of snare & bass drum (hihat left for next iteration)
    - snare: 300hz
    - bass drum: 60hz
- [X] Process the waveform (0.5s segments) and determine: 1) does it contain snare, 2) does it contain bass drum
- [] If at least 4 consecutive segments contain snare and bass drum, count it as a blast beat
- [] Plot the waveform with the blast beat segments highlighted