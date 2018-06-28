# Save-Stuff

 public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();

            
            // Init UI background
            //backgroundWorker1.DoWork += new DoWorkEventHandler(backgroundWorker1_DoWork);
            backgroundWorker1.RunWorkerCompleted += new RunWorkerCompletedEventHandler(backgroundWorker1_RunWorkerCompleted);
            backgroundWorker1.ProgressChanged += new ProgressChangedEventHandler( backgroundWorker1_ProgressChanged);
            backgroundWorker1.WorkerReportsProgress = true;

            // Run UI in separate background thread
            backgroundWorker1.RunWorkerAsync();
            //*/

            // Init Work background
            //backgroundWorker2.DoWork += new DoWorkEventHandler(backgroundWorker2_DoWork);
            backgroundWorker2.ProgressChanged += new ProgressChangedEventHandler(backgroundWorker2_ProgressChanged);
            backgroundWorker2.RunWorkerCompleted += new RunWorkerCompletedEventHandler(backgroundWorker2_RunWorkerCompleted);
            backgroundWorker2.WorkerReportsProgress = true;

            // Run UI in separate background thread
            backgroundWorker2.RunWorkerAsync();
        }


        int computeValue = 0;


        private void backgroundWorker1_DoWork(object sender, DoWorkEventArgs e)
        {
            BackgroundWorker worker = sender as BackgroundWorker;

            int p = 0;
            while (true)
            {
                System.Threading.Thread.Sleep(100);

                // Do the long-duration work here, and optionally
                // send the update back to the UI thread...
                p++;
                object param = "something"; // use this to pass any additional parameter back to the UI
                worker.ReportProgress(p, param);

                if (p > 15)
                    p = 0;
            }
        }

        // This event handler deals with the results of the background operation.
        private void backgroundWorker1_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            if (e.Cancelled == true)
            {
                label1.Text = "Canceled!";
            }
            else if (e.Error != null)
            {
                label1.Text = "Error: " + e.Error.Message;
            }
            else
            {
                label1.Text = "Done!";
            }
        }

        // This event handler updates the progress bar.
        private void backgroundWorker1_ProgressChanged(object sender, ProgressChangedEventArgs e)
        {
            //this.label2.Text = e.ProgressPercentage.ToString();
            //label1.Text = label1.Text == "......" ? ".." : "......";
            label1.Text = "";
            for (int i = 0; i < e.ProgressPercentage; i++)
            {
                label1.Text += " ";

                //label1.Text += i % 2 == 0 ? " ." : "  ";
            }
            label1.Text += ".";

            Color myColor = Color.FromArgb( (int) (e.ProgressPercentage * 2.55), Color.Blue);
            label1.ForeColor = myColor;
        }

        private void backgroundWorker2_DoWork(object sender, DoWorkEventArgs e)
        {
            BackgroundWorker worker = sender as BackgroundWorker;

            // Run main thread
            for (int i = 0; i < 30; i++)
            {
                Thread.Sleep(200);
                computeValue = i;

                worker.ReportProgress((int)(i * 3.3333f));
            }
        }


        private void backgroundWorker2_ProgressChanged(object sender, ProgressChangedEventArgs e)
        {
            label2.Text = e.ProgressPercentage.ToString();
        }

        private void backgroundWorker2_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            if (e.Cancelled == true)
            {
                label2.Text = "Canceled!";
            }
            else if (e.Error != null)
            {
                label2.Text = "Error: " + e.Error.Message;
            }
            else
            {
                label2.Text = "Done!";
            }
        }

    }
