using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;
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
                // Ensure AppData directory exists
                string appData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
                string targetDir = Path.Combine(appData, "EasyLang", "AppWeb");
                string assetsDir = Path.Combine(targetDir, "assets");
                Directory.CreateDirectory(assetsDir);

                string indexPath = Path.Combine(targetDir, "index.html");
                string logoPath = Path.Combine(assetsDir, "logo.png");

                // Extract embedded index.html
                ExtractResource("index.html", indexPath);
                // Extract embedded logo.png
                ExtractResource("assets.logo.png", logoPath);

                // Look for Microsoft Edge or Chrome
                string edgePath1 = @"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe";
                string edgePath2 = @"C:\Program Files\Microsoft\Edge\Application\msedge.exe";
                string chromePath = @"C:\Program Files\Google\Chrome\Application\chrome.exe";

                string browserExe = null;
                if (File.Exists(edgePath1)) browserExe = edgePath1;
                else if (File.Exists(edgePath2)) browserExe = edgePath2;
                else if (File.Exists(chromePath)) browserExe = chromePath;

                string fileUri = new Uri(indexPath).AbsoluteUri;
                string userDir = Path.Combine(appData, "EasyLang", "AppProfile");

                if (browserExe != null)
                {
                    ProcessStartInfo psi = new ProcessStartInfo();
                    psi.FileName = browserExe;
                    psi.Arguments = string.Format("--app=\"{0}\" --window-size=1020,840 --user-data-dir=\"{1}\"", fileUri, userDir);
                    psi.UseShellExecute = true;
                    Process.Start(psi);
                }
                else
                {
                    Process.Start(new ProcessStartInfo(fileUri) { UseShellExecute = true });
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Error launching Easy Lang: " + ex.Message,
                    "Easy Lang",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                );
            }
        }

        private static void ExtractResource(string resourceName, string outputPath)
        {
            Assembly assembly = Assembly.GetExecutingAssembly();
            using (Stream stream = assembly.GetManifestResourceStream(resourceName))
            {
                if (stream != null)
                {
                    using (FileStream fileStream = new FileStream(outputPath, FileMode.Create, FileAccess.Write))
                    {
                        stream.CopyTo(fileStream);
                    }
                }
            }
        }
    }
}
