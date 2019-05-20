package com.kuky.weatherforecaster;

import android.content.Context;
import android.content.res.Resources;

import java.io.InputStream;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;


class CloudClassifier {

    private Context ctx;
    private TensorflowImageClassifier classifier;
    CloudClassifier(Context ctx) {
        this.ctx = ctx;
        InputStream modelIs = ctx.getResources().openRawResource(R.raw.cloud_classifier);
        classifier = new TensorflowImageClassifier(
                modelIs, "conv2d_73_input:0","activation_105/Sigmoid",
                200, 7);
    }


    CloudsClassification getImageCloudsClassification(String imagePath) {
        return new CloudsClassification(classifier.classifyImage(imagePath));
    }

    CloudsClassification getImageCloudsClassification(Resources resources, int resId) {
        return new CloudsClassification(classifier.classifyImage(resources, resId));
    }

}

class CloudsClassification {
    private HashMap<String,Float> cloudsMap;
    private String[] cloudClasses = {
            "clear_sky", "cirrus", "cirrocumulus,altocumulus", "cirrostratus",
            "altostratus,nimbostratus,stratus", "cumulus", "stratocumulus"
    };

    CloudsClassification (float[] result) {
        cloudsMap = new HashMap<>();
        assert result.length == cloudClasses.length;
        for (int i = 0; i < result.length; i++) {
            cloudsMap.put(cloudClasses[i], result[i]);
        }

        cloudsMap = sortByValues(cloudsMap);
    }

    HashMap<String,Float> getCloudsScoreHashMap() {
        return cloudsMap;
    }

    private static HashMap<String,Float> sortByValues(HashMap<String,Float> map) {
        List list = new LinkedList(map.entrySet());
        // Defined Custom Comparator here
        Collections.sort(list, new Comparator() {
            public int compare(Object o1, Object o2) {
                return ((Comparable) ((Map.Entry) (o2)).getValue())
                        .compareTo(((Map.Entry) (o1)).getValue());
            }
        });

        // Here I am copying the sorted list in HashMap
        // using LinkedHashMap to preserve the insertion order
        HashMap sortedHashMap = new LinkedHashMap();
        for (Iterator it = list.iterator(); it.hasNext();) {
            Map.Entry entry = (Map.Entry) it.next();
            sortedHashMap.put(entry.getKey(), entry.getValue());
        }

        return sortedHashMap;
    }

    public String getForecast() {
        String currentClouds = cloudsMap.keySet().iterator().next();
        return getForecastByClouds(currentClouds);
    }

    private String getForecastByClouds(String currentClouds) {
        if (!Arrays.asList(cloudClasses).contains(currentClouds)) {
            return "unknown";
        }
        switch (currentClouds) {
            case "clear_sky": return "What a lovely day.";
            case "cirrus": return "The weather is going to be grand.";
            case "cirrocumulus,altocumulus": return "Prepare for slow rain arrival";
            case "cirrostratus": return "There could be some rain in the next 12 to 24 hours.";
            case "altostratus,nimbostratus,stratus": return "It is going to remain rainy/overcast.";
            case "cumulus": return "Look out for vertical growth.";
            case "stratocumulus": return "Expect no rain. The clouds are going to stay or disperse.";
        }

        return "error";
    }
}
