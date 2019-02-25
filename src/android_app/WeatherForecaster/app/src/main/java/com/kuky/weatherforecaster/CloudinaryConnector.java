package com.kuky.weatherforecaster;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;

import com.cloudinary.Cloudinary;
import com.cloudinary.android.MediaManager;
import com.cloudinary.android.callback.UploadCallback;
import com.cloudinary.utils.ObjectUtils;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public class CloudinaryConnector {

    private final String cloudName = "kuky";
    private UploadCallback uploadCallback;
    private BitmapFactory.Options bitmapOptions;
    private Context ctx;

    public static String cloudsPreset = "clouds";
    public static String othersPreset = "others";


    public CloudinaryConnector(Context appContext, UploadCallback uploadCallback) {
        Map config = new HashMap<>();
        config.put("cloud_name", cloudName);
        MediaManager.init(appContext, config);
        this.uploadCallback = uploadCallback;
        bitmapOptions = new BitmapFactory.Options();
        bitmapOptions.inScaled = false;
        ctx = appContext;
    }

    public void sendImage(String filePath, String preset) {
        filePath = scaleImage(filePath);
        try {
            MediaManager.get()
                    .upload(filePath)
                    .unsigned(preset)
                    .callback(uploadCallback)
                    .dispatch();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private String scaleImage(String filePath) {
        // scale to one side having 250, other one by ratio
        Bitmap bitmap = BitmapFactory.decodeFile(filePath, bitmapOptions);
        int w = bitmap.getWidth();
        int h = bitmap.getHeight();
        if (w * h < 500 * 1000) {
            return filePath;
        }
        float scale;
        scale = 250 / (float) (w > h ? h : w);
        w = (int) (w * scale);
        h = (int) (h * scale);
        bitmap = Bitmap.createScaledBitmap(bitmap, w, h, true);

        try {
            File tmpFile = File.createTempFile(UUID.randomUUID().toString(),null, ctx.getCacheDir());
            FileOutputStream out = new FileOutputStream(tmpFile);
            bitmap.compress(Bitmap.CompressFormat.JPEG, 90, out);
            out.flush();
            out.close();
            filePath = tmpFile.getAbsolutePath();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return filePath;

    }
}
