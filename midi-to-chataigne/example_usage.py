#!/usr/bin/env python3
"""
Example usage of the MIDI to Chataigne converter.
"""

import tempfile
from pathlib import Path
import mido
from midi_to_chataigne import ChataigneConverter


def create_example_midi():
    """Create an example MIDI file with a simple drum pattern."""
    mid = mido.MidiFile()
    
    # Drum track
    drum_track = mido.MidiTrack()
    drum_track.append(mido.Message('program_change', channel=9, program=0, time=0))
    
    # Kick drum pattern (4/4)
    for beat in range(4):
        drum_track.append(mido.Message('note_on', channel=9, note=36, velocity=100, time=0))
        drum_track.append(mido.Message('note_off', channel=9, note=36, velocity=100, time=240))
        drum_track.append(mido.Message('note_on', channel=9, note=36, velocity=80, time=0))
        drum_track.append(mido.Message('note_off', channel=9, note=36, velocity=80, time=240))
    
    # Hi-hat pattern
    hihat_track = mido.MidiTrack()
    hihat_track.append(mido.Message('program_change', channel=9, program=0, time=0))
    
    for beat in range(8):
        hihat_track.append(mido.Message('note_on', channel=9, note=42, velocity=60, time=0))
        hihat_track.append(mido.Message('note_off', channel=9, note=42, velocity=60, time=120))
    
    mid.tracks.append(drum_track)
    mid.tracks.append(hihat_track)
    
    return mid


def main():
    """Create example MIDI and convert it."""
    print("Creating example MIDI file...")
    
    # Create example MIDI
    example_midi = create_example_midi()
    midi_path = Path("example_drums.mid")
    example_midi.save(str(midi_path))
    print(f"Created {midi_path}")
    
    # Convert to Chataigne
    print("Converting to Chataigne...")
    converter = ChataigneConverter(bpm=120.0)
    success = converter.convert_midi_to_chataigne(midi_path, Path("example_drums.noisette"))
    
    if success:
        print("Conversion successful!")
        print("You can now open 'example_drums.noisette' in Chataigne")
    else:
        print("Conversion failed!")
    
    # Clean up
    midi_path.unlink()


if __name__ == "__main__":
    main()

