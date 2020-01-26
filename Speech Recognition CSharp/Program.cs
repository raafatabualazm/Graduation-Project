using System;
using System.Collections.Generic;
using System.Linq;
using Google.Cloud.Speech.V1;
using NAudio.Wave;
using System.Threading;
namespace Speech_Recognition_CSharp
{
    class Program
    {
        static void Main(string[] args)
        {
            
            var rec = true;
            var waveIn = new WaveInEvent();
            waveIn.WaveFormat = new WaveFormat(16000, 1);
            waveIn.BufferMilliseconds = 10000;
            List<byte> recorded = new List<byte>();
            string text_10 = "";
            var speech = SpeechClient.Create();
            var config = new RecognitionConfig()
            {
                Encoding = RecognitionConfig.Types.AudioEncoding.Linear16,
                SampleRateHertz = 16000,
                LanguageCode = "en-US",
                MaxAlternatives = 1
            };
            waveIn.DataAvailable += (s, a) =>
            {   
         
                
                if (a.BytesRecorded >= waveIn.WaveFormat.AverageBytesPerSecond * 10)
                {
                  
                    recorded.AddRange(a.Buffer.ToList());
                    waveIn.StopRecording();
                    rec = false;
                }
                
            };
            var copy = recorded.ToArray();
            var th1 = new Thread(() => Recognize(copy, speech, config, ref text_10));

            while (true)
            {
                rec = true;
                waveIn.StartRecording();
                while (rec) ;
                copy = recorded.ToArray();
                th1.Start();
                recorded.Clear();
                Console.WriteLine(text_10);
                th1 = new Thread(() => Recognize(copy, speech, config, ref text_10));
            }
            
        }

        static void Recognize(byte[] recording, SpeechClient speech, RecognitionConfig config, ref string s)
        {

            s = "";
            var response = speech.Recognize(config, RecognitionAudio.FromBytes(recording));
            foreach (var result in response.Results)
            {
                foreach (var alternative in result.Alternatives)
                {
                    //Console.WriteLine(alternative.Transcript);
                    s += alternative.Transcript;
                }
                if (result != response.Results.Last())
                {
                    s += " ";
                }
            }
            
            
        }
    }
}
