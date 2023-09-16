package com.example.testsocket;

import android.os.AsyncTask;
import android.util.Log;

import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.UnknownHostException;

public class SendMessage extends AsyncTask<String, Void, Void> {
    private Exception exception;

    @Override
    protected Void doInBackground(String... params) {
        try {
            try {
                Socket socket = new Socket("192.168.1.12", 8080);
                Log.d("CONNECT", "CONNECT TO SERVER");
                PrintWriter outToServer = new PrintWriter(
                        new OutputStreamWriter(
                                socket.getOutputStream()));
                outToServer.print(params[0]);
                outToServer.flush();
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (Exception e) {
            exception = e;
            return null;
        }

////      This code below is for debugging purpose
//        try {
//            Socket socket = new Socket("192.168.1.12", 8080);
//
//        } catch (UnknownHostException e) {
//            throw new RuntimeException(e);
//        } catch (IOException e) {
//            throw new RuntimeException(e);
//        }
        return null;
    }
}
