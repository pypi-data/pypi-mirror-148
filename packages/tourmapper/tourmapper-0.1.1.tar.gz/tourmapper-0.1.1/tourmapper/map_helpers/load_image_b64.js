// async function to fetch an image from a remote URL 
// and encode it as b64 string for insertion into the 
// iframe of a popup. 
// NB returns the image in the form "data:image/jpeg;base64,IMAGE_64"

if (window.screen.width < 500) {
    window.alert('This map works best on large screens.')
}

async function getBase64FromUrl(url) {
    const data = await fetch(url);
    const blob = await data.blob();
    return new Promise((resolve) => {
        const reader = new FileReader();
        reader.readAsDataURL(blob); 
        reader.onloadend = () => {
            const base64data = reader.result;   
            resolve(base64data);
        }
    });
}
