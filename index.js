require('dotenv').config();
const webhook = require('discord-webhook-node');
const hook = new webhook.Webhook(process.env.WEBHOOK);
const credentials = require('./credentials.json');
const { google } = require('googleapis');
const OAuth2 = google.auth.OAuth2;

let data = "";

main()

async function main() {
    let auth;
    try {
        auth = authorize()

    } catch (e) {
        console.error(e);
        process.exit(1);
    }
    while (true) {
        try {
            const new_data = await getVideo(auth);
            console.log("old: " + data);
            console.log("new: " + new_data);
            if (!(new_data == data)) {
                console.log('New video detected');
                hook.send(`@everyone New BotterBoyNova Video Detected! ${new_data}`);
                data = new_data;
            }
        } catch (err) {
            console.log(err);
        }
        console.log('Sleeping for 30 seconds...')
        await sleep(30000);
    }
}

function authorize() {
    const clientSecret = credentials.installed.client_secret;
    const clientId = credentials.installed.client_id;
    const redirectUrl = credentials.installed.redirect_uris[0];
    const oauth2Client = new OAuth2(clientId, clientSecret, redirectUrl);
    oauth2Client.credentials = credentials.oauth;
    return oauth2Client;
}

function getVideo(auth) {
    console.log("Getting Videos...")
    const service = google.youtube('v3')
    return new Promise((resolve, reject) => {
        service.playlistItems.list({
            auth: auth,
            playlistId: 'UU7V18bBk4EGwmxf114i1w6Q', //playlist for all videos of BotterBoyNova
            part: 'snippet'
        }, function(err, response) {
            if (err) return reject(err)
            return_data = `https://youtube.com/watch?v=${response.data.items[0].snippet.resourceId.videoId}`
            resolve(return_data)
        })
    })
}

function sleep(ms) {
    return new Promise((resolve) => {
        setTimeout(resolve, ms);
    });
}