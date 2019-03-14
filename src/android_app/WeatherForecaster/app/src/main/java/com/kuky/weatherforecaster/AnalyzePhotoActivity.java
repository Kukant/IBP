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

import java.util.Locale;
import java.util.Map;

public class AnalyzePhotoActivity extends AppCompatActivity {
    private Button btnBack;
    private CloudRecognizer cloudRecognizer;
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
        cloudinaryConnector.sendImage(filepath,
                cloudProbability > 0.8 ? CloudinaryConnector.cloudsPreset : CloudinaryConnector.othersPreset);

        textView.setText(String.format(Locale.ENGLISH, "Object on photo is %.3f cloud.", cloudProbability));
    }

    private void backToMainActivity() {
        finish();
    }

}
