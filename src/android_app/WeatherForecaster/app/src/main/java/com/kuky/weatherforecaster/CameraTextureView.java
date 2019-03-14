package com.kuky.weatherforecaster;

import android.content.Context;
import android.graphics.Rect;
import android.hardware.camera2.CameraCharacteristics;
import android.util.AttributeSet;
import android.util.Size;
import android.view.MotionEvent;
import android.view.TextureView;
import android.widget.FrameLayout;

public class CameraTextureView extends TextureView {

    protected MainActivity mainActivity;

    protected float fingerSpacing = 0;
    protected float zoomLevel = 1f;
    protected float maximumZoomLevel;
    protected Rect zoom;

    public CameraTextureView(Context context) {
        this(context, null);
    }

    public CameraTextureView(Context context, AttributeSet attrs) {
        this(context, attrs, 0);
    }

    public CameraTextureView(Context context, AttributeSet attrs, int defStyle) {
        super(context, attrs, defStyle);
    }

    public void resizeByPreview(Size previewDimensions, Size screenSize) {
        int previewHeight = previewDimensions.getWidth();
        int previewWidth = previewDimensions.getHeight();
        int screenWidth = screenSize.getWidth();
        int screenHeight = screenSize.getHeight();

        int height = (int)(previewHeight * ((float) screenWidth / previewWidth));

        FrameLayout.LayoutParams layout = new FrameLayout.LayoutParams(screenSize.getWidth(), height);

        int spaceLeft = screenHeight - height;
        layout.setMargins(0, (int)(spaceLeft * 0.3), 0, (int)(spaceLeft * 0.7));

        this.setLayoutParams(layout);

    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        try {
            Rect rect = mainActivity.characteristics.get(CameraCharacteristics.SENSOR_INFO_ACTIVE_ARRAY_SIZE);
            if (rect == null) return false;
            float currentFingerSpacing;

            if (event.getPointerCount() == 2) {
                currentFingerSpacing = getFingerSpacing(event);
                float delta = 0.05f;
                if (fingerSpacing != 0) {
                    if (currentFingerSpacing > fingerSpacing) {
                        if ((maximumZoomLevel - zoomLevel) <= delta) {
                            delta = maximumZoomLevel - zoomLevel;
                        }
                        zoomLevel = zoomLevel + delta;
                    } else if (currentFingerSpacing < fingerSpacing){
                        if ((zoomLevel - delta) < 1f) {
                            delta = zoomLevel - 1f;
                        }
                        zoomLevel = zoomLevel - delta;
                    }

                    float ratio = (float) 1 / zoomLevel;
                    int croppedWidth = rect.width() - Math.round((float)rect.width() * ratio);
                    int croppedHeight = rect.height() - Math.round((float)rect.height() * ratio);
                    zoom = new Rect(croppedWidth/2, croppedHeight/2,
                            rect.width() - croppedWidth/2, rect.height() - croppedHeight/2);

                    mainActivity.updatePreview();
                }
                fingerSpacing = currentFingerSpacing;
            }
        } catch (final Exception e) {
            e.printStackTrace();
        }

        return true;
    }

    private float getFingerSpacing(MotionEvent event) {
        float x = event.getX(0) - event.getX(1);
        float y = event.getY(0) - event.getY(1);
        return (float) Math.sqrt(x * x + y * y);
    }

}
