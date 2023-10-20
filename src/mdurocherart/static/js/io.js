async function makePostRequest(url, payload){
    let response = await fetch(
        url = url,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload)
        }
    )

    if (response.ok){
        return response
    }
    throw(
        new Error(`There was an issue loading the request, ${response.statusText} exited with code: ${response.status}`)
    )
}


async function makeGetRequest(url){
    try{
        let response = await fetch(
            url = url,
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            }
        )

        if (response.ok){
            return response
        }
        throw(
            new Error(`There was an issue loading the request, ${response.statusText} exited with code: ${response.status}`)
        )
    } catch {
        alert('There was an error processing your request, please contact support for further assistance.')
    }
}


async function redirectFromGet(url){
    let response = await makeGetRequest(url);
    if (response.ok === true){
        window.location = response.url;
    } else {
        alert('There was an issue processing your request!')
    }
}


async function redirectFromPost(url, payload){
    let response = await makePostRequest(url, payload);
    if (response.ok === true){
        window.location = response.url;
    } else {
        alert('There was an issue processing your request!')
    };
}
