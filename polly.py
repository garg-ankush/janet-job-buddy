import boto3

def convert_text_to_speech(script, voice_id='Joanna', output_format='mp3', output_file='output.mp3'):
    # Create an instance of the Polly client
    polly = boto3.client('polly')
    
    try:
        # Request Polly to synthesize speech
        response = polly.synthesize_speech(
            Text=script,
            OutputFormat=output_format,
            VoiceId=voice_id
        )
        
        # Save the audio to a file
        with open(output_file, 'wb') as f:
            f.write(response['AudioStream'].read())
        
        print(f'Successfully converted the script to speech. Saved as {output_file}')
        
    except Exception as e:
        print(f'Error occurred: {str(e)}')
