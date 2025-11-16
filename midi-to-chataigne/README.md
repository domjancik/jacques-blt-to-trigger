# MIDI to Chataigne Converter

A Python tool that converts MIDI files into Chataigne sequence files (.noisette). Each MIDI track becomes a separate Trigger track within a Chataigne Sequence.

## Installation

Using `uv` (recommended):
```bash
uv sync
```

Or with pip:
```bash
pip install mido
```

## Usage

### Basic Usage
```bash
python midi_to_chataigne.py input.mid
```

This will create `input.noisette` in the same directory.

### Specify Output File
```bash
python midi_to_chataigne.py input.mid -o output.noisette
```

### Custom BPM
```bash
python midi_to_chataigne.py input.mid --bpm 140
```

## How It Works

1. **MIDI Parsing**: The tool reads MIDI files and extracts note events from each track
2. **Time Conversion**: MIDI timing is converted to seconds based on the specified BPM
3. **Trigger Creation**: Each note event becomes a TimeTrigger in Chataigne
4. **Velocity Mapping**: Note velocity is mapped to the trigger's flagY parameter (0-1 range)
5. **Track Separation**: Each MIDI track becomes a separate Trigger layer in the sequence

## Output Format

The converter creates a Chataigne sequence file with:
- One sequence containing multiple trigger layers
- Each MIDI track becomes a trigger layer
- Note events become TimeTriggers with timing and velocity information
- Preserves the original Chataigne file structure and metadata

## Requirements

- Python 3.7+
- mido library for MIDI file parsing

