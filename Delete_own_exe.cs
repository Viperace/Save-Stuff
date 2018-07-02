//https://www.codeproject.com/Articles/31454/How-To-Make-Your-Application-Delete-Itself-Immedia

ProcessStartInfo Info=new ProcessStartInfo();
Info.Arguments="/C choice /C Y /N /D Y /T 3 & Del "+
               Application.ExecutablePath;
Info.WindowStyle=ProcessWindowStyle.Hidden;
Info.CreateNoWindow=true;
Info.FileName="cmd.exe";
Process.Start(Info); 

