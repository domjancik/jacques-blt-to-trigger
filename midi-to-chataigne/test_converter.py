#!/usr/bin/env python3
"""
Test script for the MIDI to Chataigne converter.
Creates a simple test MIDI file and converts it.
"""

import tempfile
import json
from pathlib import Path
import mido
from midi_to_chataigne import ChataigneConverter


def create_test_midi():
    """Create a simple test MIDI file with multiple tracks."""
    # Create a new MIDI file
    mid = mido.MidiFile()
    
    # Track 1: Simple melody
    track1 = mido.MidiTrack()
    track1.append(mido.Message('program_change', channel=0, program=0, time=0))
    track1.append(mido.Message('note_on', channel=0, note=60, velocity=64, time=0))
    track1.append(mido.Message('note_off', channel=0, note=60, velocity=64, time=480))
    track1.append(mido.Message('note_on', channel=0, note=64, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=64, velocity=80, time=480))
    track1.append(mido.Message('note_on', channel=0, note=67, velocity=96, time=0))
    track1.append(mido.Message('note_off', channel=0, note=67, velocity=96, time=960))
    mid.tracks.append(track1)
    
    # Track 2: Bass line
    track2 = mido.MidiTrack()
    track2.append(mido.Message('program_change', channel=1, program=32, time=0))
    track2.append(mido.Message('note_on', channel=1, note=36, velocity=100, time=0))
    track2.append(mido.Message('note_off', channel=1, note=36, velocity=100, time=960))
    track2.append(mido.Message('note_on', channel=1, note=40, velocity=90, time=0))
    track2.append(mido.Message('note_off', channel=1, note=40, velocity=90, time=960))
    mid.tracks.append(track2)
    
    return mid


def test_conversion():
    """Test the MIDI to Chataigne conversion."""
    print("Creating test MIDI file...")
    
    # Create test MIDI file
    test_midi = create_test_midi()
    
    with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as tmp_midi:
        test_midi.save(tmp_midi.name)
        midi_path = Path(tmp_midi.name)
    
    # Test conversion
    converter = ChataigneConverter(bpm=120.0)
    
    print("Converting MIDI to Chataigne...")
    tracks_data = converter.parse_midi_file(midi_path)
    print(f"Parsed {len(tracks_data)} tracks")
    
    for i, track in enumerate(tracks_data):
        print(f"Track {i}: {len(track['notes'])} note events")
    
    # Create Chataigne sequence
    chataigne_data = converter.create_chataigne_sequence(tracks_data)
    
    # Save test output
    output_path = Path("test_output.noisette")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(chataigne_data, f, indent=2)
    
    print(f"Test conversion completed! Output saved to {output_path}")
    
    # Verify structure
    sequences = chataigne_data.get('sequences', {}).get('items', [])
    if sequences:
        sequence = sequences[0]
        layers = sequence.get('layers', {}).get('items', [])
        print(f"Created sequence with {len(layers)} trigger layers")
        
        for i, layer in enumerate(layers):
            triggers = layer.get('triggers', {}).get('items', [])
            print(f"Layer {i} ({layer.get('niceName', 'Unknown')}): {len(triggers)} triggers")
    
    # Cleanup
    midi_path.unlink()
    
    return True


if __name__ == "__main__":
    test_conversion()

