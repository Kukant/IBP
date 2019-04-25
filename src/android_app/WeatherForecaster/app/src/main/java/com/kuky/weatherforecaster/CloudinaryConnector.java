package com.kuky.weatherforecaster;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.util.Log;

import com.cloudinary.Cloudinary;
import com.cloudinary.android.MediaManager;
import com.cloudinary.android.callback.UploadCallback;
import com.cloudinary.utils.ObjectUtils;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;
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


    public CloudinaryConnector(Context appContext) {
        Map config = new HashMap<>();
        config.put("cloud_name", cloudName);
        try {
            MediaManager.init(appContext, config);
        } catch (java.lang.IllegalStateException e) {
            Log.e("CLOUDINARY CONNECTOR", "already initialized");
        }

        bitmapOptions = new BitmapFactory.Options();
        bitmapOptions.inScaled = false;
        ctx = appContext;
    }

    public void sendImage(String filePath, String preset, String cloudsCategory) {
        filePath = scaleImage(filePath);
        try {
            MediaManager.get()
                    .upload(filePath)
                    .unsigned(preset)
                    .option("public_id", getUniqueFilename(cloudsCategory))
                    .dispatch();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private String getUniqueFilename(String cloudsCategory) {
        DateFormat df = new SimpleDateFormat("yyMMddHHmmss");
        String date = df.format(Calendar.getInstance().getTime());
        String ranStr = UUID.randomUUID().toString().replace("-", "").substring(0, 6);
        return cloudsCategory + "-" + date + "-" + ranStr;
    }

    private String scaleImage(String filePath) {
        // scale to one side having 250, other one by ratio
        Bitmap bitmap = BitmapFactory.decodeFile(filePath, bitmapOptions);
        int w = bitmap.getWidth();
        int h = bitmap.getHeight();

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
