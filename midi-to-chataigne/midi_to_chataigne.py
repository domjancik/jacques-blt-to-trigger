#!/usr/bin/env python3
"""
MIDI to Chataigne Converter

This tool converts MIDI files into Chataigne sequence files (.noisette).
Each MIDI track becomes a separate Trigger track within a Chataigne Sequence.
"""

import json
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple
import mido


class ChataigneConverter:
    """Converts MIDI files to Chataigne sequence format."""
    
    def __init__(self, bpm: float = 120.0):
        self.bpm = bpm
        self.tempo = mido.bpm2tempo(bpm)
        
    def parse_midi_file(self, midi_path: Path) -> List[Dict[str, Any]]:
        """Parse MIDI file and extract note events from each track."""
        try:
            midi_file = mido.MidiFile(str(midi_path))
            tracks_data = []
            
            for track_idx, track in enumerate(midi_file.tracks):
                track_notes = []
                current_time = 0.0
                
                for msg in track:
                    current_time += mido.tick2second(msg.time, midi_file.ticks_per_beat, self.tempo)
                    
                    if msg.type == 'note_on' and msg.velocity > 0:
                        # Note start
                        track_notes.append({
                            'time': current_time,
                            'note': msg.note,
                            'velocity': msg.velocity,
                            'type': 'note_on'
                        })
                    elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                        # Note end
                        track_notes.append({
                            'time': current_time,
                            'note': msg.note,
                            'velocity': 0,
                            'type': 'note_off'
                        })
                
                if track_notes:  # Only add tracks that have notes
                    tracks_data.append({
                        'track_index': track_idx,
                        'name': f'Track {track_idx + 1}',
                        'notes': track_notes
                    })
            
            return tracks_data
            
        except Exception as e:
            print(f"Error parsing MIDI file: {e}")
            return []
    
    def create_chataigne_sequence(self, tracks_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a Chataigne sequence structure from MIDI track data."""
        
        # Base Chataigne structure
        chataigne_data = {
            "metaData": {
                "version": "1.9.24",
                "versionNumber": 67864
            },
            "projectSettings": {
                "containers": {
                    "dashboardSettings": {
                        "parameters": [{
                            "value": "",
                            "controlAddress": "/showDashboardOnStartup",
                            "enabled": False
                        }]
                    },
                    "customDefinitions": {}
                }
            },
            "dashboardManager": {"viewOffset": [0, 0], "viewZoom": 1.0},
            "parrots": {"viewOffset": [0, 0], "viewZoom": 1.0},
            "layout": {
                "mainLayout": {
                    "type": 1,
                    "width": 1707,
                    "height": 870,
                    "direction": 2,
                    "shifters": [{
                        "type": 1,
                        "width": 1707,
                        "height": 870,
                        "direction": 2,
                        "shifters": [{
                            "type": 1,
                            "width": 1707,
                            "height": 403,
                            "direction": 1,
                            "shifters": [{
                                "type": 1,
                                "width": 307,
                                "height": 403,
                                "direction": 2,
                                "shifters": [{
                                    "type": 0,
                                    "width": 307,
                                    "height": 209,
                                    "currentContent": "Modules",
                                    "tabs": [{"name": "Modules"}]
                                }, {
                                    "type": 0,
                                    "width": 307,
                                    "height": 187,
                                    "currentContent": "Custom Variables",
                                    "tabs": [{"name": "Custom Variables"}]
                                }]
                            }, {
                                "type": 0,
                                "width": 398,
                                "height": 403,
                                "currentContent": "State Machine",
                                "tabs": [{"name": "State Machine"}, {"name": "Dashboard"}, {"name": "Module Router"}, {"name": "Morpher"}]
                            }, {
                                "type": 0,
                                "width": 990,
                                "height": 403,
                                "currentContent": "Inspector",
                                "tabs": [{"name": "Inspector"}]
                            }]
                        }, {
                            "type": 1,
                            "width": 1707,
                            "height": 461,
                            "direction": 1,
                            "shifters": [{
                                "type": 0,
                                "width": 178,
                                "height": 461,
                                "currentContent": "Sequences",
                                "tabs": [{"name": "Sequences"}]
                            }, {
                                "type": 0,
                                "width": 1043,
                                "height": 461,
                                "currentContent": "Sequence Editor",
                                "tabs": [{"name": "Sequence Editor"}]
                            }, {
                                "type": 0,
                                "width": 474,
                                "height": 461,
                                "currentContent": "Logger",
                                "tabs": [{"name": "Help"}, {"name": "Logger"}, {"name": "Warnings"}]
                            }]
                        }]
                    }]
                },
                "windows": None
            },
            "modules": {"viewOffset": [0, 0], "viewZoom": 1.0},
            "customVariables": {"viewOffset": [0, 0], "viewZoom": 1.0},
            "states": {
                "viewOffset": [42, -59],
                "viewZoom": 0.53125,
                "transitions": {"hideInEditor": True, "viewOffset": [0, 0], "viewZoom": 1.0},
                "comments": {"hideInEditor": True, "viewOffset": [42, -59], "viewZoom": 0.53125}
            },
            "sequences": {
                "items": [],
                "viewOffset": [0, 0],
                "viewZoom": 1.0
            },
            "routers": {"viewOffset": [0, 0], "viewZoom": 1.0}
        }
        
        # Create sequence with layers for each MIDI track
        sequence = {
            "parameters": [{
                "value": "",
                "controlAddress": "/ltcSyncModule",
                "enabled": False
            }],
            "niceName": "MIDI Sequence",
            "type": "Sequence",
            "layers": {
                "hideInEditor": True,
                "items": [],
                "viewOffset": [0, 0],
                "viewZoom": 1.0
            },
            "cues": {"hideInEditor": True, "viewOffset": [0, 0], "viewZoom": 1.0},
            "editing": True
        }
        
        # Convert each MIDI track to a Trigger layer
        for track_data in tracks_data:
            trigger_layer = self.create_trigger_layer(track_data)
            sequence["layers"]["items"].append(trigger_layer)
        
        chataigne_data["sequences"]["items"].append(sequence)
        return chataigne_data
    
    def create_trigger_layer(self, track_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a Trigger layer from MIDI track data."""
        
        # Group notes by time to create triggers
        note_events = {}
        for note in track_data['notes']:
            time_key = round(note['time'], 3)  # Round to avoid floating point issues
            if time_key not in note_events:
                note_events[time_key] = []
            note_events[time_key].append(note)
        
        # Create triggers for each time point
        triggers = []
        for time_key, events in sorted(note_events.items()):
            # Calculate flagY based on note velocity (normalized to 0-1)
            note_on_events = [event for event in events if event['type'] == 'note_on']
            if note_on_events:
                max_velocity = max(event['velocity'] for event in note_on_events)
                flag_y = min(max_velocity / 127.0, 1.0)
            else:
                # If no note_on events at this time, use a default value
                flag_y = 0.5
            
            trigger = {
                "parameters": [
                    {"value": time_key, "controlAddress": "/time"},
                    {"value": flag_y, "controlAddress": "/flagY"}
                ],
                "niceName": f"Trigger {len(triggers) + 1}",
                "type": "TimeTrigger",
                "consequences": {"viewOffset": [0, 0], "viewZoom": 1.0}
            }
            triggers.append(trigger)
        
        # Create the trigger layer
        trigger_layer = {
            "parameters": [{"value": len(triggers), "controlAddress": "/listSize"}],
            "niceName": track_data['name'],
            "type": "Trigger",
            "triggers": {
                "hideInEditor": True,
                "items": triggers,
                "viewOffset": [0, 0],
                "viewZoom": 1.0
            }
        }
        
        return trigger_layer
    
    def convert_midi_to_chataigne(self, midi_path: Path, output_path: Path) -> bool:
        """Convert MIDI file to Chataigne sequence file."""
        print(f"Converting {midi_path} to {output_path}")
        
        # Parse MIDI file
        tracks_data = self.parse_midi_file(midi_path)
        if not tracks_data:
            print("No MIDI tracks found or error parsing file")
            return False
        
        print(f"Found {len(tracks_data)} tracks with notes")
        
        # Create Chataigne sequence
        chataigne_data = self.create_chataigne_sequence(tracks_data)
        
        # Write output file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(chataigne_data, f, indent=None, separators=(',', ':'))
            print(f"Successfully created {output_path}")
            return True
        except Exception as e:
            print(f"Error writing output file: {e}")
            return False


def main():
    """Main entry point for the converter."""
    parser = argparse.ArgumentParser(
        description="Convert MIDI files to Chataigne sequence files"
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Input MIDI file path"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output Chataigne file path (default: input_file.noisette)"
    )
    parser.add_argument(
        "--bpm",
        type=float,
        default=120.0,
        help="BPM for timing conversion (default: 120.0)"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not args.input_file.exists():
        print(f"Error: Input file {args.input_file} does not exist")
        sys.exit(1)
    
    if args.input_file.suffix.lower() not in ['.mid', '.midi']:
        print(f"Error: Input file must be a MIDI file (.mid or .midi)")
        sys.exit(1)
    
    # Set output file path
    if args.output:
        output_path = args.output
    else:
        output_path = args.input_file.with_suffix('.noisette')
    
    # Convert file
    converter = ChataigneConverter(bpm=args.bpm)
    success = converter.convert_midi_to_chataigne(args.input_file, output_path)
    
    if success:
        print("Conversion completed successfully!")
    else:
        print("Conversion failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
