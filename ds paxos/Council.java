// Java implementation for the council
// It contains two classes : Council and MemberHandler
// Save file as Council.java

import java.io.*;
import java.util.*;
import java.net.*;

// Council class
public class Council
{
	public static ArrayList<Socket> memberList = new ArrayList<Socket>();
	public static int max_num_proposal = 0;
	public static String msg;
	public static int counter = 0;
	public static int port;
	public static boolean wait = true;

	public static void main(String[] args) throws IOException
	{
		// server is listening on inputted port
		ServerSocket ss = new ServerSocket(Integer.parseInt(args[0]));

		// Storing the port for specific test cases
		port = Integer.parseInt(args[0]);
		
		// running infinite loop for getting members
		while (true)
		{
			Socket s = null;
			
			try
			{
				// socket object to receive incoming client requests
				s = ss.accept();
				
				System.out.println("A new member is connected : " + s);
				
				// obtaining input and out streams
				DataInputStream dis = new DataInputStream(s.getInputStream());
				DataOutputStream dos = new DataOutputStream(s.getOutputStream());
				
				System.out.println("Assigning new thread for this member");

				// create a new thread object
				Thread t = new MemberHandler(s, dis, dos, memberList);

				// Add members to a list
                memberList.add(s);
				
				// Invoking the start() method
				t.start();

			}
			catch (Exception e){
				e.printStackTrace();
			}
		}
	}
}

// ClientHandler class
class MemberHandler extends Thread
{
	public final DataInputStream dis;
	public final DataOutputStream dos;
	final Socket s;
    ArrayList<Socket> memberList;

	// Constructor
	public MemberHandler(Socket s, DataInputStream dis, DataOutputStream dos, ArrayList<Socket> members)
	{
		this.s = s;
		this.dis = dis;
		this.dos = dos;
        this.memberList = members;
	}

	@Override
	public void run()
	{
		try {
			// Server is ready for a proposer
			if (s == Council.memberList.get(0)){
				Timer timer = new Timer();
				TimerTask task = new ready();
				timer.schedule(task, 3000);
			}

			// Prepare
			if (dis.readUTF().equals("Prepare")){
				int received = dis.readInt();
				String value = dis.readUTF();
				prepare(received, value);
			} 

			// Proposer (Propose)
			proposer(dis, dos);

			// Consensus
			consensus(dis, dos);

		} catch (IOException e) {
			e.printStackTrace();
		}
	
		try
		{
			// closing resources
			this.dis.close();
			this.dos.close();
			
		}catch(IOException e){
			e.printStackTrace();
		}
	}

	public void prepare(int id, String Value) throws IOException {
		if(id > Council.max_num_proposal){
			Council.max_num_proposal = id;
			Council.msg = Value;
			for (int i = 0; i < Council.memberList.size(); i++) {
				DataOutputStream Output = new DataOutputStream(Council.memberList.get(i).getOutputStream());
				Output.writeInt(Council.max_num_proposal);
				Output.writeUTF(Council.msg);
			}
		}
	}

	public void proposer(DataInputStream dis, DataOutputStream dos) throws IOException {
		String promise = dis.readUTF();
		if(promise.equals("Promise")) {
			dos.writeUTF("Accept?");
			String accept = dis.readUTF();
			if (accept.equals("Yes")) {
				Council.counter++;
			}
		}
	}

	public void consensus(DataInputStream dis, DataOutputStream dos) throws IOException {
		Council.max_num_proposal = dis.readInt();
		Council.msg = dis.readUTF();
		FileWriter myWriter = new FileWriter("output.txt");
		double agreement = (double) Council.memberList.size()/2;
		if (Council.counter >= Math.round(agreement)){
			myWriter.write("Consensus passed");
		} else {
			myWriter.write("Consensus failed");
		}
		myWriter.close();
	}
}

class ready extends TimerTask{
    public void run() {
		int max = Council.memberList.size();
        int member = (int) Math.random()*(max);
		if (Council.port == 7000){
			member = 1;
		}
		DataOutputStream Output;
		try {
			for (int i = 0; i < max; i++){
				Output = new DataOutputStream(Council.memberList.get(i).getOutputStream());
				if (i == member){
					Output.writeUTF("Invoke");
				} else {
					Output.writeUTF(" ");
				}
			}
		} catch (IOException e) {
		}
    }
}