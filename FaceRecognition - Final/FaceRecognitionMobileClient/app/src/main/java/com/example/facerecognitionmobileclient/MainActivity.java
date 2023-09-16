package com.example.facerecognitionmobileclient;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.util.Base64;
import android.util.Log;
import android.view.SurfaceView;
import android.widget.ImageView;
import android.widget.Toast;

import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.JavaCameraView;
import org.opencv.android.OpenCVLoader;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.imgproc.Imgproc;
import org.opencv.videoio.VideoCapture;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.lang.reflect.Array;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.Socket;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.Arrays;


public class MainActivity extends AppCompatActivity  {

    private ImageView mImageView;
    private boolean mIsReceiving = false;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mImageView = (ImageView) findViewById(R.id.image_view);

        final String SERVER_IP = "192.168.234.2"; // Server IP address
        final int SERVER_PORT = 9999; // Server port number
        final int BUFFER_SIZE = 65536; // Buffer size in bytes
        final int CLIENT_PORT = 9090;


        Thread receiveVideoThread = new Thread(new Runnable() {
            @Override
            public void run() {

                DatagramSocket udpSocket = null;
                try {
                    udpSocket = new DatagramSocket(CLIENT_PORT);
                } catch (SocketException e) {
                    throw new RuntimeException(e);
                }
                byte[] buffer = new byte[BUFFER_SIZE];
                DatagramPacket packet = new DatagramPacket(buffer, buffer.length);

                String message = "hello";
                byte[] data = message.getBytes();
                InetAddress serverAddress = null;
                try {
                    serverAddress = InetAddress.getByName(SERVER_IP);
                } catch (UnknownHostException e) {
                    throw new RuntimeException(e);
                }
                DatagramPacket sendPacket = new DatagramPacket(data, data.length, serverAddress, SERVER_PORT);
                try {
                    udpSocket.send(sendPacket);
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }

//              Received video frame from server and display them
                try {
                    byte[] videoBuffer = new byte[BUFFER_SIZE];
                    DatagramPacket videoFramePacket = new DatagramPacket(videoBuffer, videoBuffer.length);
                    while (true) {
                        udpSocket.receive(videoFramePacket);
                        String lText = new String(videoBuffer, 0, videoFramePacket.getLength());
                        byte[] decodeDataImg = Base64.decode(lText, Base64.DEFAULT);
                        Bitmap bitmap = BitmapFactory.decodeByteArray(decodeDataImg, 0, decodeDataImg.length);
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                mImageView.setImageBitmap(bitmap);
                            }
                        });

                    }
                } catch (Exception e){
                    e.printStackTrace();
                }

            }
        });
        receiveVideoThread.start();

    }
}
