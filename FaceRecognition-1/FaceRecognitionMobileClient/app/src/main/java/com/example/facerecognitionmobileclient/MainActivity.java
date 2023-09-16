package com.example.facerecognitionmobileclient;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.util.Log;
import android.view.SurfaceView;
import android.widget.Toast;

import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.JavaCameraView;
import org.opencv.android.OpenCVLoader;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.imgproc.Imgproc;

import java.net.Socket;


public class MainActivity extends AppCompatActivity implements CameraBridgeViewBase.CvCameraViewListener2 {

    private static String TAG = "MainActivity";
    JavaCameraView javaCameraView;
    Mat mRGBA, mRGBAT;

    private static final int MY_CAMERA_REQUEST_CODE = 100;
    int activeCamera = CameraBridgeViewBase.CAMERA_ID_BACK;
    BaseLoaderCallback baseLoaderCallback = new BaseLoaderCallback(MainActivity.this) {
        @Override
        public void onManagerConnected(int status) {
            switch (status) {
                case BaseLoaderCallback.SUCCESS:
                {
                    javaCameraView.enableView();
                    break;
                }
                default:
                {
                    super.onManagerConnected(status);
                    break;
                }
            }
            super.onManagerConnected(status);
        }
    };

    private void initializeCamera(JavaCameraView javaCameraView, int activeCamera) {
        javaCameraView.setCameraPermissionGranted();
        javaCameraView.setCameraIndex(activeCamera);
        javaCameraView.setVisibility(CameraBridgeViewBase.VISIBLE);
        javaCameraView.setCvCameraViewListener(this);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if(requestCode == MY_CAMERA_REQUEST_CODE){
            if(grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "camera permission granted", Toast.LENGTH_SHORT).show();
                initializeCamera(javaCameraView, activeCamera);
            }
            else {
                Toast.makeText(this, "camera permission denied", Toast.LENGTH_SHORT).show();
            }
        }
    }

    //    static {
//        if(OpenCVLoader.initDebug()) {
//            Log.d(TAG, "OpenCV is Configured or Connected Successfully");
//        }
//        else {
//            Log.d(TAG, "OpenCV is not working");
//        }
//    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        javaCameraView = (JavaCameraView) findViewById(R.id.my_camera_view);
//        javaCameraView.setVisibility(SurfaceView.VISIBLE);
//        javaCameraView.setCvCameraViewListener(MainActivity.this);
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
        == PackageManager.PERMISSION_GRANTED) {
            Log.d(TAG, "Permission granted");
            initializeCamera(javaCameraView, activeCamera);
        }
        else {
            Log.d(TAG, "Permission prompt");
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.CAMERA}, MY_CAMERA_REQUEST_CODE);
        }
    }

    @Override
    public void onCameraViewStarted(int width, int height) {
        mRGBA = new Mat(height, width, CvType.CV_8UC4);
    }

    @Override
    public void onCameraViewStopped() {
        mRGBA.release();
    }

    @Override
    public Mat onCameraFrame(CameraBridgeViewBase.CvCameraViewFrame inputFrame) {
        mRGBA = inputFrame.rgba();
        mRGBAT = mRGBA.t();
        Core.flip(mRGBA.t(), mRGBAT, 1);
        Imgproc.resize(mRGBAT, mRGBAT, mRGBA.size());
        return mRGBAT;
    }

    @Override
    public void onPointerCaptureChanged(boolean hasCapture) {
//        super.onPointerCaptureChanged(hasCapture);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        if(javaCameraView != null) {
            javaCameraView.disableView();
        }
    }

    @Override
    protected void onPause() {
        super.onPause();

        if(javaCameraView != null) {
            javaCameraView.disableView();
        }
    }

    @Override
    protected void onResume() {
        super.onResume();

        if(OpenCVLoader.initDebug()) {
            Log.d(TAG, "OpenCV is Configured or Connected Successfully");
            baseLoaderCallback.onManagerConnected(BaseLoaderCallback.SUCCESS);
        }
        else {
            Log.d(TAG, "OpenCV is not working");
            OpenCVLoader.initAsync(OpenCVLoader.OPENCV_VERSION, this, baseLoaderCallback);
        }
    }
}
