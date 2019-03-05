package com.kuky.weatherforecaster;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.SurfaceTexture;
import android.hardware.camera2.CameraAccessException;
import android.hardware.camera2.CameraCaptureSession;
import android.hardware.camera2.CameraCharacteristics;
import android.hardware.camera2.CameraDevice;
import android.hardware.camera2.CameraManager;
import android.hardware.camera2.CaptureRequest;
import android.hardware.camera2.params.StreamConfigurationMap;
import android.os.Handler;
import android.os.HandlerThread;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Size;
import android.view.Surface;
import android.view.TextureView;
import android.view.View;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.RelativeLayout;
import android.widget.Toast;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Calendar;
import java.util.UUID;
import java.lang.*;

public class MainActivity extends AppCompatActivity {

    private Button btnCapture;
    private TextureView textureView;

    private String cameraId;
    private CameraDevice cameraDevice;
    private CameraCaptureSession cameraCaptureSession;
    private CaptureRequest.Builder captureRequestBuilder;
    private Size previewDimensions;
    private Toast toast;

    CameraDevice.StateCallback stateCallBack = new CameraDevice.StateCallback() {
        @Override
        public void onOpened(@NonNull CameraDevice camera) {
            cameraDevice = camera;
            createCameraPreview();
        }

        @Override
        public void onDisconnected(@NonNull CameraDevice camera) {
            cameraDevice.close();
        }

        @Override
        public void onError(@NonNull CameraDevice camera, int error) {
            cameraDevice.close();
            cameraDevice = null;
        }
    };

    TextureView.SurfaceTextureListener textureListener = new TextureView.SurfaceTextureListener() {
        @Override
        public void onSurfaceTextureAvailable(SurfaceTexture surface, int width, int height) {
            openCamera();
        }

        @Override
        public void onSurfaceTextureSizeChanged(SurfaceTexture surface, int width, int height) {

        }

        @Override
        public boolean onSurfaceTextureDestroyed(SurfaceTexture surface) {
            return false;
        }

        @Override
        public void onSurfaceTextureUpdated(SurfaceTexture surface) {

        }
    };


    private File file;
    private static final int REQUEST_CAMERA_PERMISSION = 200;
    private Handler mBackgroundHandler;
    private HandlerThread mBackgroundThread;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        btnCapture = findViewById(R.id.btnCapture);
        assert btnCapture != null;

        btnCapture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                takePicture();
            }
        });

        textureView = findViewById(R.id.textureView);
        assert textureView != null;
        textureView.setSurfaceTextureListener(textureListener);
    }

    private File getPhotoTmpFile() {
        DateFormat df = new SimpleDateFormat("HH-mm-ss");
        String date = df.format(Calendar.getInstance().getTime());
        File outputDir = getApplicationContext().getCacheDir(); // context being the Activity pointer
        try {
            return File.createTempFile("cloud_"+ UUID.randomUUID().toString() + date, ".jpg", outputDir);
        } catch (IOException e) {
            e.printStackTrace();
        }

        return null;
    }

    private void lockPreview() {
        try {
            cameraCaptureSession.capture(captureRequestBuilder.build(),
                    null, mBackgroundHandler);
        } catch (CameraAccessException e) {
            e.printStackTrace();
        }
    }

    private void unlockPreview() {
        try {
            cameraCaptureSession.setRepeatingRequest(captureRequestBuilder.build(),
                    null, mBackgroundHandler);
        } catch (CameraAccessException e) {
            e.printStackTrace();
        }
    }

    private void takePicture() {
        try {
            lockPreview();
            file = getPhotoTmpFile();
            FileOutputStream outputPhoto = new FileOutputStream(file);
            textureView.getBitmap().compress(Bitmap.CompressFormat.JPEG, 100, outputPhoto);
            outputPhoto.close();
            processFile(file.getAbsolutePath());
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            unlockPreview();
        }
    }

    private Size getIdealSize(Size[] cameraSizes) {
        // ideal size is the one that will cover the most of the screen
        Size displaySize = getDisplaySize();
        int screenWidth = displaySize.getWidth();
        int screenHeight = displaySize.getHeight();

        int bestSizeIdx = 0;
        int bestRating = Integer.MAX_VALUE;
        for (int i = 0; i < cameraSizes.length; i++) {
            Size c = cameraSizes[i];
            int r = Math.abs(screenWidth - c.getWidth()) + Math.abs(screenHeight - c.getHeight());
            if (r < bestRating) {
                bestRating = r;
                bestSizeIdx = i;
            }
        }

        return cameraSizes[bestSizeIdx];
    }

    private void createCameraPreview() {
        try {
            SurfaceTexture texture = textureView.getSurfaceTexture();
            assert texture != null;
            texture.setDefaultBufferSize(previewDimensions.getWidth(), previewDimensions.getHeight());
            Surface surface = new Surface(texture);
            captureRequestBuilder = cameraDevice.createCaptureRequest(CameraDevice.TEMPLATE_PREVIEW);
            captureRequestBuilder.addTarget(surface);
            cameraDevice.createCaptureSession(Arrays.asList(surface), new CameraCaptureSession.StateCallback() {
                @Override
                public void onConfigured(@NonNull CameraCaptureSession session) {
                    if (cameraDevice == null) {
                        return;
                    }
                    cameraCaptureSession = session;
                    updatePreview();
                }

                @Override
                public void onConfigureFailed(@NonNull CameraCaptureSession session) {
                }
            }, null);
        } catch (CameraAccessException e) {
            e.printStackTrace();
        }
    }

    private void updatePreview() {
        if (cameraDevice == null) {
            showToast("Error on updatePreview.");
        }
        captureRequestBuilder.set(CaptureRequest.CONTROL_MODE, CaptureRequest.CONTROL_MODE_AUTO);
        try {
            cameraCaptureSession.setRepeatingRequest(captureRequestBuilder.build(), null, mBackgroundHandler);
        } catch (CameraAccessException e) {
            e.printStackTrace();
        }
    }

    private void updateTextureViewSize() {
        int previewHeight = previewDimensions.getWidth();
        int previewWidth = previewDimensions.getHeight();
        Size screenSize = getDisplaySize();
        int screenWidth = screenSize.getWidth();
        int screenHeight = screenSize.getHeight();

        int height = (int)(previewHeight * ((float) screenWidth / previewWidth));

        FrameLayout.LayoutParams layout = new FrameLayout.LayoutParams(screenSize.getWidth(), height);

        int spaceLeft = screenHeight - height;
        layout.setMargins(0, (int)(spaceLeft * 0.3), 0, (int)(spaceLeft * 0.7));

        textureView.setLayoutParams(layout);

    }

    private void openCamera() {
        CameraManager manager = (CameraManager) getSystemService(Context.CAMERA_SERVICE);
        try {
            cameraId = manager.getCameraIdList()[0];
            CameraCharacteristics characteristics = manager.getCameraCharacteristics(cameraId);
            StreamConfigurationMap map = characteristics.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP);
            assert map != null;
            Size []previewSizes = map.getOutputSizes(SurfaceTexture.class);
            previewDimensions = getIdealSize(previewSizes);
            updateTextureViewSize();
            // check realtime permission if run higher API 23
            if (ActivityCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this, new String[]{
                        Manifest.permission.CAMERA,
                        Manifest.permission.WRITE_EXTERNAL_STORAGE
                }, REQUEST_CAMERA_PERMISSION);
                return;
            }
            manager.openCamera(cameraId, stateCallBack, null);

        } catch (CameraAccessException e) {
            e.printStackTrace();
        }
    }

    private void closeCamera() {
        if (cameraDevice != null) {
            cameraDevice.close();
            cameraDevice = null;
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        if (requestCode == REQUEST_CAMERA_PERMISSION) {
            if (grantResults[0] != PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "Permission needed.", Toast.LENGTH_SHORT).show();
                finish();
            }
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        startBackgroundThread();
        if (textureView.isAvailable()) {
            openCamera();
        } else {

            textureView.setSurfaceTextureListener(textureListener);
        }
    }

    @Override
    protected void onPause() {
        if (toast != null) {
            toast.cancel();
        }

        closeCamera();
        stopBackgroundThread();
        super.onPause();
    }

    @Override
    protected void onStop() {
        super.onStop();
        closeCamera();
        stopBackgroundThread();
    }

    private void stopBackgroundThread() {
        if (mBackgroundThread != null) {
            mBackgroundThread.quitSafely();
            try {
                mBackgroundThread.join();
                mBackgroundThread = null;
                mBackgroundHandler = null;
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    private void startBackgroundThread() {
        mBackgroundThread = new HandlerThread("Camera Background");
        mBackgroundThread.start();
        mBackgroundHandler = new Handler(mBackgroundThread.getLooper());
    }

    private void showToast(String toastText) {
        if (toast != null) {
            toast.cancel();
        }
        toastText += " (v" + getAppVersionName() + ")";
        (toast = Toast.makeText(MainActivity.this, toastText, Toast.LENGTH_SHORT)).show();
    }

    private void processFile(String filepath) {
        analyzePhotoActivity(filepath);
    }

    private void analyzePhotoActivity(String filepath) {
        Intent intent = new Intent(MainActivity.this, AnalyzePhotoActivity.class);
        intent.putExtra("filepath", filepath);
        startActivity(intent);
        btnCapture.setEnabled(true);
    }

    private String getAppVersionName(){
        PackageManager manager = this.getPackageManager();
        String ret;
        try {
            ret = manager.getPackageInfo(this.getPackageName(), PackageManager.GET_ACTIVITIES).versionName;
        } catch (PackageManager.NameNotFoundException e) {
            e.printStackTrace();
            ret = "err";
        }
        return ret;
    }

    private Size getDisplaySize() {
        RelativeLayout rootView = findViewById(R.id.rootView);
        return new Size(rootView.getWidth(), rootView.getHeight());
    }
}
