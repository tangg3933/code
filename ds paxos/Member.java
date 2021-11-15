// Java implementation for members of the council
// Save file as Member.java

import java.io.*;
import java.net.*;
import java.util.*;

// Member class
public class Member
{
	public static boolean occupy = true;
	public static int ID = 0;
	public static boolean wait = false;
	public static void main(String[] args) throws IOException
	{
		try
		{
			Scanner scn = new Scanner(System.in);
			
			// getting localhost ip
			InetAddress ip = InetAddress.getByName("localhost");
	
			// establish the connection with inputted port
			Socket s = new Socket(ip, Integer.parseInt(args[1]));
	
			// obtaining input and out streams 
			DataInputStream dis = new DataInputStream(s.getInputStream());
			DataOutputStream dos = new DataOutputStream(s.getOutputStream());

			while (true) {

				// Proposer (Prepare)
				if (dis.readUTF().equals("Invoke")){
					System.out.println(args[0] + " Proposer");
					dos.writeUTF("Prepare");
					int max = ID + 10;
					int min = ID;
					int newID = (int)Math.floor(Math.random()*(max-min+1)+min);
					dos.writeInt(newID);
					dos.writeUTF("msg");
				} else {
					if (Integer.parseInt(args[1]) == 5060) {
						System.out.println(args[0] + " Proposer");
					} else {
						System.out.println(args[0] + " Receiver");
					}
					dos.writeUTF("Waiting");
				}
				
				// Acceptor (Promise)
				int received = dis.readInt();
				String accepted_value = dis.readUTF();
				Timer timer = new Timer();
				TimerTask task = new delayAccept();

				// Promise sent successfully or not
				int Send = (int)(Math.random()*2);
				int response = (int)(Math.random()*2);

				// Test cases
				if (Integer.parseInt(args[1]) == 6010){
					Send = 0;
				} else if (Integer.parseInt(args[1]) == 5010){
					Send = 1;
					response = 1;
				} else if (Integer.parseInt(args[1]) == 2050){
					Send = 1;
				} else if (Integer.parseInt(args[1]) == 3000){
					Send = 0;
				} else if (Integer.parseInt(args[1]) == 4020){
					Send = 1;
				}  

				// Members of the council
				if (args[0].equals("M1")) {
					// Implementation for M1
					// M1 accepts instantly
					ID = Members(ID, received, accepted_value, dis, dos);
					System.out.println(args[0] + " accept proposal id " + received);
				} else if (args[0].equals("M2")) {
					// Implementation for M2
					if (Send == 0){
						// M2 accepts instantly
						ID = Members(ID, received, accepted_value, dis, dos);
						System.out.println(args[0] + " accept proposal id " + received);
					} else {
						timer.schedule(task, 4000);
						System.out.println(args[0] + " 4s response time");
						if (response == 0) {
							// M2 delayed accept
							while (true){
								Send = (int)Math.floor(Math.random()*2);
								if (wait) {
									ID = Members(ID, received, accepted_value, dis, dos);
									System.out.println(args[0] + " accept proposal id " + received);
									break;
								}
							}
						} else {
							// M2 delay fail to accept
							while (true){
								Send = (int)Math.floor(Math.random()*2);
								if (wait) {
									ID = Failed(ID, received, "Unresponsive", dis, dos);
									System.out.println(args[0] + " failed to accept proposal id " + received);
									break;
								}
							}
						}
					}
				} else if (args[0].equals("M3")) {
					// Implementation for M3
					if (Send == 0){
						// M3 delay accept
						timer.schedule(task, 2050);
						System.out.println(args[0] + " 2s response time");
						while (true){
							Send = (int)Math.floor(Math.random()*2);
							if (wait) {
								ID = Members(ID, received, accepted_value, dis, dos);
								System.out.println(args[0] + " accept proposal id " + received);
								break;
							}
						}
					} else {
						// M3 fail to accept instantly
						ID = Failed(ID, received, "Unresponsive", dis, dos);
						System.out.println(args[0] + " failed to accept proposal id " + received);
					}
				} else {
					// Implementation for M4-9 
					int time = (int)(Math.random()*9) + 1;

					if (Integer.parseInt(args[1]) == 6010){
						time = 1;
					}
					
					// Random timer set for M4-9
					timer.schedule(task, time*1000);
					System.out.println(args[0] + " " + time + "s response time");

					if (Integer.parseInt(args[1]) == 5060){
						System.out.println(args[0] + " already accept proposal");
					}

					if (Send == 0){
						// M4-9 delay accept
						while (true){
							Send = (int)Math.floor(Math.random()*2);
							if (wait) {
								ID = Members(ID, received, accepted_value, dis, dos);
								System.out.println(args[0] + " accept proposal id " + received);
								break;
							}
						}
					} else {
						// M4-9 delay fail to accept
						while (true){
							Send = (int)Math.floor(Math.random()*2);
							if (wait) {
								ID = Failed(ID, received, accepted_value , dis, dos);
								System.out.println(args[0] + " failed to accept proposal id " + received);
								break;
							}
						}
					}
				}

				timer.cancel();
				s.close();
				break;
			}

			// closing resources
			scn.close();
			dis.close();
			dos.close();
		}catch(Exception e){
			e.printStackTrace();
		}
	}

	// Members that accept the promise
	public static int Members(int id, int newId, String value, DataInputStream input, DataOutputStream output) throws IOException {
		if (newId > id) {
			id = newId;
			output.writeUTF("Promise");
			if (input.readUTF().equals("Accept?"))
			{
				output.writeUTF("Yes");
			}
			output.writeInt(id);
			output.writeUTF(value);
		}
		return id;
	}

	// Members that don't accept the promise
	public static int Failed(int id, int newId, String value, DataInputStream input, DataOutputStream output) throws IOException {
		if (newId > id) {
			id = newId;
			output.writeUTF("Promise");
			if (input.readUTF().equals("Accept?"))
			{
				output.writeUTF("No");
			}
			output.writeInt(id);
			output.writeUTF(value);
		}
		return id;
	}
}

// Delay members acceptance
class delayAccept extends TimerTask {
	public void run() {
		Member.wait = true;
	}
}
