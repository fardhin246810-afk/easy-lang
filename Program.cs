using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

namespace EasyLangApp
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            try
            {
                string baseDir = AppDomain.CurrentDomain.BaseDirectory;
                string indexPath = Path.Combine(baseDir, "index.html");

                if (!File.Exists(indexPath))
                {
                    MessageBox.Show(
                        "Could not locate index.html. Please ensure EasyLang.exe is placed in the project folder.",
                        "Easy Lang - File Missing",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Warning
                    );
                    return;
                }

                // Check for Microsoft Edge or Chrome to run in clean standalone --app mode
                string edgePath1 = @"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe";
                string edgePath2 = @"C:\Program Files\Microsoft\Edge\Application\msedge.exe";
                string chromePath = @"C:\Program Files\Google\Chrome\Application\chrome.exe";

                string browserExe = null;
                if (File.Exists(edgePath1)) browserExe = edgePath1;
                else if (File.Exists(edgePath2)) browserExe = edgePath2;
                else if (File.Exists(chromePath)) browserExe = chromePath;

                string fileUri = new Uri(indexPath).AbsoluteUri;

                if (browserExe != null)
                {
                    string appData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
                    string userDir = Path.Combine(appData, "EasyLang", "AppProfile");
                    
                    ProcessStartInfo psi = new ProcessStartInfo();
                    psi.FileName = browserExe;
                    psi.Arguments = string.Format("--app=\"{0}\" --window-size=1020,840 --user-data-dir=\"{1}\"", fileUri, userDir);
                    psi.UseShellExecute = true;
                    Process.Start(psi);
                }
                else
                {
                    // Fallback to default shell handler
                    Process.Start(new ProcessStartInfo(fileUri) { UseShellExecute = true });
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Error launching Easy Lang: " + ex.Message,
                    "Easy Lang - Error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                );
            }
        }
    }
}
