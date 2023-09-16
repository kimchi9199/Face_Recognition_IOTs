package com.example.testsocket;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.os.AsyncTask;
import android.view.SurfaceHolder;
import android.view.SurfaceView;

import java.io.IOException;
import java.io.InputStream;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

public class VideoStreamTask extends AsyncTask<Void, byte[], Void> {
    private final String host;
    private final int port;
    private final SurfaceView surfaceView;

    public VideoStreamTask(String host, int port, SurfaceView surfaceView) {
        this.host = host;
        this.port = port;
        this.surfaceView = surfaceView;
    }

    @Override
    protected Void doInBackground(Void... voids) {
        try(Socket socket = new Socket(host, port);
        InputStream inputStream = socket.getInputStream()) {

            // Set byte order to little endian
            ByteBuffer byteBuffer = ByteBuffer.allocate(4).order(ByteOrder.LITTLE_ENDIAN);

            while (!isCancelled()) {
                // Read frame size from socket
                inputStream.read(byteBuffer.array());
                int size = byteBuffer.getInt(0);

                if (size > 0) {
                    // Read frame data from socket
                    byte[] data = new byte[size];
                    inputStream.read(data);

                    // Publish frame data to UI thread for display
                    publishProgress(data);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    @Override
    protected void onProgressUpdate(byte[]... values) {
        super.onProgressUpdate(values);
        SurfaceHolder holder = surfaceView.getHolder();

        // Lock surface view and draw frame
        Canvas canvas = holder.lockCanvas();
        BitmapFactory.Options options = new BitmapFactory.Options();
        options.inSampleSize = 2;
        Bitmap bitmap = BitmapFactory.decodeByteArray(values[0], 0, values[0].length, options);
        if (bitmap != null && !bitmap.isRecycled()) {
            canvas.drawBitmap(bitmap, 0, 0, null);
        }
        holder.unlockCanvasAndPost(canvas);
    }
}
