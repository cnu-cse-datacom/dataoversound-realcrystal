package com.example.sound.devicesound;

import android.media.AudioFormat;
import android.media.AudioRecord;
import android.media.MediaRecorder;
import android.util.Log;

import org.apache.commons.math3.complex.Complex;
import org.apache.commons.math3.transform.*;

import java.util.ArrayList;

public class Listentone {

    int HANDSHAKE_START_HZ = 4096;
    int HANDSHAKE_END_HZ = 5120 + 1024;

    int START_HZ = 1024;
    int STEP_HZ = 256;
    int BITS = 4;

    int FEC_BYTES = 4;

    private int mAudioSource = MediaRecorder.AudioSource.MIC;
    private int mSampleRate = 44100;
    private int mChannelCount = AudioFormat.CHANNEL_IN_MONO;
    private int mAudioFormat = AudioFormat.ENCODING_PCM_16BIT;
    private float interval = 0.1f;

    private int mBufferSize = AudioRecord.getMinBufferSize(mSampleRate, mChannelCount, mAudioFormat);

    public AudioRecord mAudioRecord = null;
    int audioEncodig;
    boolean startFlag;
    FastFourierTransformer transform;

    public Listentone(){

        transform = new FastFourierTransformer(DftNormalization.STANDARD);
        startFlag = false;
        mAudioRecord = new AudioRecord(mAudioSource, mSampleRate, mChannelCount, mAudioFormat, mBufferSize);
        mAudioRecord.startRecording();

        int blocksize = findPowerSize((int)(long)Math.round(interval/2*mSampleRate));
        short[] buffer = new short[blocksize];
        int bufferedReadResult = mAudioRecord.read(buffer, 0, blocksize);

    }
    

    private double findFrequency(double[] toTransform)
    {
        int len = toTransform.length;
        double[] real = new double[len];
        double[] img = new double[len];
        double realNum;
        double imgNum;
        double[] mag = new double[len];

        Complex[] complx = transform.transform(toTransform, TransformType.FORWARD);
        Double[] freq = this.fftfreq(complx.length, 1);

        for(int i = 0; i<complx.length; i++){
            realNum = complx[i].getReal();
            imgNum = complx[i].getImaginary();
            mag[i] = Math.sqrt((realNum * realNum) + (imgNum + imgNum));
        }
    }

    private int findPowerSize(int x) {
        int mul = (int)(long)Math.round(Math.log(x)/Math.log(2));

        int caseA=square((mul-1));
        int caseB=square((mul));
        int caseC=square((mul+1));

        int case_A = Math.abs((caseA-x));
        int case_B = Math.abs((caseB-x));
        int case_C = Math.abs((caseC-x));
        
        int min = Math.min(case_A, Math.min(case_B, case_C));

        if(min==case_A){
            return caseA;
        }
        else if(min==case_B){
            return caseB;
        }
        else{
            return caseC;
        }

    }

    private int square(int x){
        int a = 2;
        for(int i=1; i<=x; i++){
            a *= 2;
        }
        return a;
    }


}
