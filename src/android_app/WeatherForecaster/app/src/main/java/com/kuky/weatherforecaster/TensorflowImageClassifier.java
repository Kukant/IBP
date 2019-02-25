package com.kuky.weatherforecaster;

import android.content.res.Resources;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;

import org.tensorflow.contrib.android.TensorFlowInferenceInterface;

import java.io.InputStream;

public class TensorflowImageClassifier {
    private int imageSize;
    private TensorFlowInferenceInterface tfExecutor;
    private String inputLayerName;
    private String outputLayerName;
    private int outputSize;
    private BitmapFactory.Options bitmapOptions;

    TensorflowImageClassifier(InputStream model, String inputLayerName, String outputLayerName, int imageSize, int outputSize) {
        tfExecutor = new TensorFlowInferenceInterface(model);
        this.inputLayerName = inputLayerName;
        this.outputLayerName = outputLayerName;
        this.imageSize = imageSize;
        this.outputSize = outputSize;
        bitmapOptions = new BitmapFactory.Options();
        bitmapOptions.inScaled = false;
    }

    public float[] classifyImage(Resources resources, int imgId) {
        float []pixels = getPixels(resources, imgId);

        return classifyPixels(pixels);
    }

    public float[] classifyImage(String imagePath) {
        float []pixels = getPixels(imagePath);

        return classifyPixels(pixels);
    }

    private float[] classifyPixels(float[] pixels) {
        tfExecutor.feed(inputLayerName, pixels, 1, imageSize, imageSize, 3);
        tfExecutor.run(new String[] {outputLayerName});
        float []output = new float[outputSize];
        tfExecutor.fetch(outputLayerName, output);

        return output;
    }

    private float[] getPixels(Resources resources, int imgId) {
        Bitmap bitmap = BitmapFactory.decodeResource(resources, imgId, bitmapOptions);

        return extractPixelsFromBitmap(bitmap);
    }

    private float[] getPixels(String imagePath) {
        Bitmap bitmap = BitmapFactory.decodeFile(imagePath, bitmapOptions);

        return extractPixelsFromBitmap(bitmap);
    }

    private float[] extractPixelsFromBitmap(Bitmap bitmap) throws IllegalArgumentException {
        bitmap = Bitmap.createScaledBitmap(bitmap, imageSize, imageSize, true);

        float[] normalized = new float[imageSize * imageSize * 3];
        int i = 0;
        for (int y = 0; y < imageSize; y++) {
            for (int x = 0; x < imageSize; x++) {
                // tf needs BGR format
                int pixel = bitmap.getPixel(x, y);
                normalized[i++] = (float) Color.blue(pixel) / 255;
                normalized[i++] = (float) Color.green(pixel) / 255;
                normalized[i++] = (float) Color.red(pixel) / 255;
            }
        }

        return normalized;
    }
}
