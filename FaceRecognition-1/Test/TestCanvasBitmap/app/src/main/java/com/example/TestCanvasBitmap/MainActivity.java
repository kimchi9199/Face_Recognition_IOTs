package com.example.TestCanvasBitmap;

import androidx.appcompat.app.AppCompatActivity;

import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.media.Image;
import android.os.Bundle;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.widget.ImageView;

public class MainActivity extends AppCompatActivity {

    private SurfaceView surfaceView;
    private ImageView imageView;
    private SurfaceHolder surfaceHolder;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        surfaceView = findViewById(R.id.surfaceView);
        surfaceHolder = surfaceView.getHolder();
        imageView = findViewById(R.id.imageView2);
    }

    public void buttonDrawCanvas(View view) {
        Bitmap bitmap = Bitmap.createBitmap(surfaceView.getWidth(), surfaceView.getHeight(),
                Bitmap.Config.ARGB_8888);

        Paint paint = new Paint();
        paint.setColor(Color.RED);
        paint.setAntiAlias(true);
        paint.setStyle(Paint.Style.STROKE);
        paint.setStrokeWidth(5);

        Canvas canvas = new Canvas(bitmap);
        canvas.drawCircle(bitmap.getWidth()/2, bitmap.getHeight()/2,
                bitmap.getWidth()/5, paint);

        imageView.setImageBitmap(bitmap);

        canvas = surfaceHolder.lockCanvas();
        canvas.drawCircle(bitmap.getWidth()/2, bitmap.getHeight()/2,
                bitmap.getWidth()/5, paint);
        surfaceHolder.unlockCanvasAndPost(canvas);
    }
}