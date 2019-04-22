package com.kuky.weatherforecaster;

import android.content.Context;
import android.support.test.InstrumentationRegistry;
import android.support.test.runner.AndroidJUnit4;

import org.junit.Test;
import org.junit.runner.RunWith;

import static org.junit.Assert.assertEquals;


@RunWith(AndroidJUnit4.class)
public class CloudClassifierTest {
    @Test
    public void classifyClouds() {
        Context appContext = InstrumentationRegistry.getTargetContext();

        CloudClassifier cr = new CloudClassifier(appContext);
        CloudsClassification cc = cr.getImageCloudsClassification(appContext.getResources(), R.raw.cloud);

    }
}
