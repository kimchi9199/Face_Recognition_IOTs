package com.example.testsocket;

import androidx.appcompat.app.AppCompatActivity;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.SurfaceView;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toolbar;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class MainActivity extends AppCompatActivity {
    private static final String HOST = "192.168.0.166";
    private static final int PORT = 9999;
    private static final int WIDTH = 400;
    private static final int HEIGHT = 300;

    private VideoStreamTask videoStreamTask;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

//        SurfaceView surfaceView = findViewById(R.id.surfaceview);
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        ImageView imageView = findViewById(R.id.imageView);

        try {
            DatagramSocket clientSocket = new DatagramSocket();
            byte[] receiveData = new byte[65536];

            InetAddress IPAddress = InetAddress.getByName("localhost");
            DatagramPacket sendPacket = new DatagramPacket("Hello from client".getBytes(), "Hello from client".getBytes().length, IPAddress, PORT);
            clientSocket.send(sendPacket);

            while (true) {
                DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
                clientSocket.receive(receivePacket);

                byte[] imageBytes = receivePacket.getData();
                ByteArrayInputStream bis = new ByteArrayInputStream(imageBytes);
                byte[] decodedBytes = android.util.Base64.decode(new String(imageBytes).trim(), android.util.Base64.DEFAULT);
                Bitmap bitmap = BitmapFactory.decodeByteArray(decodedBytes, 0, decodedBytes.length);
                if (bitmap == null) {
                    continue;
                }
                imageView.setImageBitmap(bitmap);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

//        // Start video stream task
//        videoStreamTask = new VideoStreamTask(HOST, PORT, surfaceView);
//        videoStreamTask.executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
////        final EditText editText = (EditText) findViewById(R.id.edtText);
////        Button button = (Button) findViewById(R.id.button);
////
////        button.setOnClickListener(new View.OnClickListener() {
////            @Override
////            public void onClick(View view) {
////                new SendMessage().execute(editText.getText().toString());
////                editText.getText().clear();
////            }
////        });
//    }

//    @Override
//    protected void onDestroy() {
//        super.onDestroy();
//
//        // Stop video stream task
//        if (videoStreamTask != null) {
//            videoStreamTask.cancel(true);
//            videoStreamTask = null;
//        }
//    }
}