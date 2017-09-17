package crypto;


import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.math.BigInteger;
import java.util.Base64;
import java.util.Scanner;

import javax.imageio.ImageIO;
//import com.sun.org.apache.xerces.internal.impl.dv.util.Base64;
 
 
public class Stegano {
	public static void embed(String dirName,String fileName,String writeFileName,String formatFile,String hideText)
	{
		try {
			ByteArrayOutputStream baos=new ByteArrayOutputStream(1000);
			BufferedImage img = ImageIO.read(new File(dirName,fileName));
			
			ImageIO.write(img,formatFile, baos);
			baos.flush();
	 
			String base64String=Base64.getEncoder().encodeToString(baos.toByteArray());
			baos.close();
			
			
			byte[] bytearray = Base64.getDecoder().decode((base64String));
			//System.out.println(bytearray.length);
			String S = null;
			//String hideText = "";
			int cnt = 0;
			for(int i=100;i<bytearray.length-100;i++)
			{
				//System.out.println(bytearray[i]);
				if(cnt < hideText.length())
				{
					S = String.format("%8s", Integer.toBinaryString(bytearray[i] & 0xFF)).replace(' ', '0');
					int l = S.length();
					S = S.substring(0,l-1) + hideText.charAt(cnt);
					cnt++;
					bytearray[i] = (byte)Integer.parseInt(S,2);
				}
					
				//System.out.println(bytearray[i]);
			}
	 
			BufferedImage imag=ImageIO.read(new ByteArrayInputStream(bytearray));
			ImageIO.write(imag, formatFile, new File(dirName,writeFileName));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	public static String reveal(String dirName,String writeFileName,String formatFile,int len)
	{
		try {
			ByteArrayOutputStream baos=new ByteArrayOutputStream(1000);
			BufferedImage img = ImageIO.read(new File(dirName,writeFileName));
			
			ImageIO.write(img,formatFile, baos);
			baos.flush();
	 
			String base64String=Base64.getEncoder().encodeToString(baos.toByteArray());
			baos.close();
			
			
			byte[] bytearray = Base64.getDecoder().decode((base64String));
			//System.out.println(bytearray.length);
			String S = null;
			StringBuilder orgmsg = new StringBuilder();
			//String hideText = "";
			int cnt = 0;
			for(int i=100;i<bytearray.length-100;i++)
			{
				//System.out.println(bytearray[i]);
				if(cnt < len)
				{
					S = String.format("%8s", Integer.toBinaryString(bytearray[i] & 0xFF)).replace(' ', '0');
					int l = S.length();
					orgmsg.append(S.charAt(l-1));
					cnt++;
				}
			}
			System.out.println(orgmsg.toString());
			return orgmsg.toString();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return "";
		
	}
	public static void main(String[] args) throws IOException{
		String dirName = "D:\\CSE 5381 Information Security 2\\Assignment\\Final Assignment";
		String fileName = "fred.bmp";
		String writeFileName = "fred1.bmp";
		String formatFile = "bmp";
		String hideText = "";
		String message = "";
		String messageCoded = "sivakumaran3555 27/06/1989";
		String outmessage = "";
		Scanner in = new Scanner(System.in);
		
		System.out.println("File Directory:");
		message = in.nextLine();
		if(!message.isEmpty())
			dirName=message;
		
		System.out.println("Original Source File Name:");
		message = in.nextLine();
		if(!message.isEmpty())
			fileName=message;
		
		System.out.println("Modified File Name:");
		message = in.nextLine();
		if(!message.isEmpty())
			writeFileName = message;
		
		System.out.println("File format:");
		message = in.nextLine();
		if(!message.isEmpty())
			formatFile = message;
		
		message = "";
		System.out.println("Enter text to be hidden:");
		System.out.println("Allowed characters A-Z 0-9 space ! # $ % & . - ,");
		message = in.nextLine();
		if(message.isEmpty())
			message = messageCoded;
		
		System.out.println("Given text:"+ message );
		
	    //Hide message
		hideText = getMapping(message);
		System.out.println("Binary format:");
		System.out.println(hideText);
		embed(dirName,fileName,writeFileName,formatFile,hideText);
		System.out.println("Steganography done");
		System.out.println();
		System.out.println();
		//Get message
		System.out.println("Examining Image for Steganography");
		outmessage = reveal(dirName,writeFileName,formatFile,hideText.length());
		System.out.println("Binary format:");
		System.out.println(outmessage);
		String clearText = getUnMapping(outmessage);
		System.out.println("Hidden Message:");
		System.out.println(clearText);
	}
	public static String getUnMapping(String outmessage) {
		// TODO Auto-generated method stub
		int lim = outmessage.length();
		int i = 0;
		String msg = "";
		char letter;
		StringBuilder strblr = new StringBuilder();
		while(i<lim)
		{
			msg = outmessage.substring(i, i+6);
			int val = Integer.parseInt(msg, 2);
			i = i+6;
			
			if((val>=1)&&(val<=26))
			{
				letter = (char)(val + 64);
				strblr.append(letter);
			}
			else if((val>=27)&&(val<=36))
			{
				letter = (char)(val + 21);
				strblr.append(letter);
			}
			else
			{
				letter = (char)(val - 5);
				strblr.append(letter);
			}
		}
		return strblr.toString();
	}
	public static String getMapping(String input) {
		// TODO Auto-generated method stub
		
		StringBuilder inputblr = new StringBuilder();
	    for(int i = 0; i < input.length(); i++)
	    {
	    	int asc = (int)input.charAt(i);
	    	int ind = 0;
	    	if(asc<=47 && asc>=32)
	    	{
	    		//37,38... 52
	    		ind = (asc - 32) + 37;
	    	}
	    	else if((asc<=90 && asc>=65) || (asc<=122 && asc>=97))
	    	{
	    		if(asc<=90 && asc>=65)
	    		{
	    			ind = (asc - 65) + 1; 
	    		}
	    		else
	    		{
	    			ind = (asc - 97) + 1;
	    		}
	    	}
	    	else if(asc<=57 && asc>=48)
	    	{
	    		ind = (asc - 48) + 27;
	    	}
	    	else
	    	{
	    		System.out.println("Inavlid Character");
	    	}
	    	String str = Integer.toBinaryString(ind);
	    	//System.out.println(str);
	    	//System.out.println(String.format("%06d",new Integer(str)));
	    	inputblr.append(String.format("%06d",new Integer(str)));
	    }
		
		return inputblr.toString();
	}
}
