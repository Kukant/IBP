package com.kuky.weatherforecaster;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import com.cloudinary.android.callback.ErrorInfo;
import com.cloudinary.android.callback.UploadCallback;

import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

public class AnalyzePhotoActivity extends AppCompatActivity {
    private Button btnBack;
    private CloudRecognizer cloudRecognizer;
    private CloudClassifier cloudClassifier;
    private CloudinaryConnector cloudinaryConnector;
    private TextView textView;
    private ImageView imageView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_analyze_photo);

        btnBack = findViewById(R.id.btnBack);
        assert btnBack != null;
        btnBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                backToMainActivity();
            }
        });

        textView = findViewById(R.id.textView);
        imageView = findViewById(R.id.imageView);

        cloudRecognizer = new CloudRecognizer(getApplicationContext());

        cloudinaryConnector = new CloudinaryConnector(getApplicationContext());

        cloudClassifier = new CloudClassifier(getApplicationContext());

        Bundle bundle = getIntent().getExtras();
        assert bundle != null;

        String filepath = bundle.getString("filepath");

        showImage(filepath);
        analyzeImage(filepath);
    }

    private void showImage(String filepath) {
        Bitmap imgBitmap = BitmapFactory.decodeFile(filepath);
        imageView.setImageBitmap(imgBitmap);
    }


    private void analyzeImage(String filepath) {
        float cloudProbability = cloudRecognizer.IsCloud(filepath);
        String clouds_category;
        if (cloudProbability > 0.5) {
            CloudsClassification cloudsClassification = cloudClassifier.getImageCloudsClassification(filepath);
            HashMap<String,Float> cloudsMap = cloudsClassification.getCloudsScoreHashMap();
            String text = "";
            clouds_category = cloudsMap.keySet().iterator().next();
            for (Map.Entry<String, Float> item : cloudsMap.entrySet()) {
                String key = item.getKey();
                Float value = item.getValue();
                text += String.format(Locale.ENGLISH, "%.2f %% %s\n",  value*100, key);
            }
            textView.setText(text);
            textView.setTextAlignment(View.TEXT_ALIGNMENT_TEXT_START);
        } else {
            clouds_category = "nocloud";
            textView.setText(String.format(Locale.ENGLISH, "Object on photo is not a sky. (%.2f %% sure)",  (1 - cloudProbability)*100));
            textView.setTextAlignment(View.TEXT_ALIGNMENT_CENTER);
        }

        cloudinaryConnector.sendImage(
                filepath,
                cloudProbability > 0.5 ? CloudinaryConnector.cloudsPreset : CloudinaryConnector.othersPreset,
                clouds_category);
    }

    private void backToMainActivity() {
        finish();
    }

}
