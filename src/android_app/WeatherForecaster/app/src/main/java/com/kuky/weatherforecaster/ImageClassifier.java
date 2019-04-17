package com.kuky.weatherforecaster;

import android.content.res.Resources;

import java.io.InputStream;

public interface ImageClassifier {
    float[] classifyImage(String imagePath);
    float[] classifyImage(Resources resources, int imgId);
}
