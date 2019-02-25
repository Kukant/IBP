package com.kuky.weatherforecaster;

import android.content.Context;
import android.content.res.Resources;
import android.util.Log;

import java.io.InputStream;


public class CloudRecognizer {
    private Context ctx;
    private TensorflowImageClassifier classifier;

    CloudRecognizer (Context ctx) {
        this.ctx = ctx;
        InputStream modelIs = ctx.getResources().openRawResource(R.raw.cloud_recognizer);
        classifier = new TensorflowImageClassifier(
                modelIs, "conv2d_1_input","activation_3/Sigmoid",
                200, 1);
    }

    public float IsCloud(String imagePath) {
        return classifier.classifyImage(imagePath)[0];
    }

    public float IsCloud(Resources resources, int resId) {
        return classifier.classifyImage(resources, resId)[0];
    }

}
