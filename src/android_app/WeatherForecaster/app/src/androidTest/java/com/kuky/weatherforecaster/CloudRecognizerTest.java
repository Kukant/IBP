package com.kuky.weatherforecaster;

import android.content.Context;
import android.support.test.InstrumentationRegistry;
import android.support.test.runner.AndroidJUnit4;
import android.util.Log;

import org.junit.Test;
import org.junit.runner.RunWith;

import static org.junit.Assert.assertEquals;


@RunWith(AndroidJUnit4.class)
public class CloudRecognizerTest {
    @Test
    public void recognizeClouds() {
        Context appContext = InstrumentationRegistry.getTargetContext();

        CloudRecognizer cr = new CloudRecognizer(appContext);
        assertEquals(cr.IsCloud(appContext.getResources(), R.raw.cloud), 0.9, 0.2);
        assertEquals(cr.IsCloud(appContext.getResources(), R.raw.nocloud), 0.2, 0.2);
    }
}
