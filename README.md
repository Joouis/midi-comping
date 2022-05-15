### Environments

#### Toolkits

- Conda@4.10.1
- Python@3.8.11

#### Dependencies

- miditoolkit@0.1.16

### Instructions

#### Arguments

- `-i`: input midi file
- `-o`: output midi file

```python
# Generate midi with comping tracks
python main.py -i ./zh_pop/zhpop_117.mid -o output.mid
```

### Notes

#### Drum

Pitch of drum means tone in MuseScore.

- Bass: 36
- Tom: 38, 40
- Clap: 39
- Snare: 41
- Hi-hat: 42

#### Program

Program number of instruments except drum in MuseScore.

| Program number | Instrument    |
| -------------- | ------------- |
| 1              | Piano         |
| 32             | Contrabass    |
| 33             | Electric Bass |
| 34             | Bass Guitar   |

