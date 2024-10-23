# Install required packages
# !pip install magenta pydub

import time
import magenta
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.protobuf import generator_pb2
from magenta.protobuf import music_pb2
from pydub import AudioSegment
from IPython.display import Audio, display
import tempfile
import random

# Helper function to generate a melody
def generate_melody(generator, num_steps=128, temperature=1.0):
    # Define the sequence generation request
    input_sequence = music_pb2.NoteSequence()  # Empty input leads to random melody
    generator_options = generator_pb2.GeneratorOptions()
    generator_options.args['temperature'].float_value = temperature

    # Generate a sequence
    generated_sequence = generator.generate(input_sequence, generator_options)
    return generated_sequence

# Function to play the generated melody as an audio segment
def play_generated_melody(sequence):
    # Temporary MIDI file storage
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mid')
    magenta.music.sequence_proto_to_midi_file(sequence, temp_file.name)
    
    # Convert MIDI to Audio using pydub (you may need an external tool like fluidsynth)
    audio_segment = AudioSegment.from_file(temp_file.name, format="mid")
    
    # Play audio in the notebook (works in IPython/Jupyter)
    display(Audio(data=audio_segment.raw_data, rate=audio_segment.frame_rate))
    
    temp_file.close()

# Setup MelodyRNN (using a pre-trained model)
def setup_generator():
    # Downloading pre-trained Melody RNN model (use any compatible model)
    bundle = magenta.music.read_bundle_file('/path_to_pretrained_model/melody_rnn.mag')
    generator = melody_rnn_sequence_generator.create_sequence_generator(bundle)
    return generator

# Main loop to generate continually changing music
def continuous_music_generation():
    generator = setup_generator()
    
    while True:
        # Generate a new melody snippet
        temperature = random.uniform(0.8, 1.2)  # Add randomness to temperature for variation
        generated_sequence = generate_melody(generator, temperature=temperature)
        
        # Play the generated melody
        play_generated_melody(generated_sequence)
        
        # Wait for some time before generating the next sequence
        time.sleep(10)  # Adjust time interval as needed

# Run the continuous music generation process
continuous_music_generation()
