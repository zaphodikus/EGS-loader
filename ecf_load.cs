Dictionary<String, int> ecfimport = new Dictionary<String, int>(); //Allow for String => int lookup
Dictionary<int, String> ecfimportOrig = new Dictionary<int, String>(); //Allow for int => string lookup
public void LoadEcf()
{
   var source = "../../Configuration/Config_Example.ecf"; //Path to file
   if (debug == 1)
   {
       GameAPI.Console_Write(thismodsub.ToUpper() + " DEBUG: Attempting to load ecf file from : " + source + " :: " + getSource(source));
   }
   using (var input = File.OpenText(getSource(source)))
   {
       string s = "";
       s = input.ReadToEnd();
       string[] st = s.Split('{');
       foreach (string ss in st)
       {
           int te = -1;
           string ts = "";
           string[] sb = ss.Split(',', '\n');
           foreach (string se in sb)
           {
               if (te == -1 && se.Contains("Id:"))
               {
                   try
                   {
                       te = int.Parse(se.Split(':')[1].Replace("\n", "").Replace(" ", ""));
                   }
                   catch
                   {
                   }
               } else if (ts == "" && se.Contains("Name:"))
               {
                   try
                   {
                       ts = se.Split(':')[1].Replace("\n", "").Replace(" ", "");
                   }
                   catch
                   {
                   }
               }
               if (te != -1 && ts != "")
               {
                   break;
               }
           }
           if (te != -1 && ts != "")
           {
               if (ecfimport.ContainsKey(ts.ToLower()))
               {
                   if (debug == 1)
                   {
                       GameAPI.Console_Write(thismodsub.ToUpper() + " Notice: collision on ecf " + ts + " : " + te);
                   }
               }
               else
               {
                   ecfimport.Add(ts.ToLower().Replace("\r", ""), te);
                   ecfimportOrig.Add(te, ts.ToLower().Replace("\r", ""));
               }
           }
       }
   }
   if (debug == 1)
   {
       GameAPI.Console_Write(thismodsub.ToUpper() + " DEBUG: loaded file " + config.LastUsedFile);
   }
}