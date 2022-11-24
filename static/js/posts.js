console.log("helloooo");

function copyPost(id) {
    navigator.clipboard.writeText(id);
    console.log(`ID '${id}' copied`);
    M.toast({html: `ID '${id}' copied`});
}


function addComment(id) {
    console.log("adding comment to post " + id);
    content = document.getElementById("commentInput-" + id).value;
    console.log(content);
    const url='/comments/' + id;
    jQuery.post(url, {content: content});
    M.toast({html: `Comment added`});
    document.getElementById("commentInput-" + id).value = "";
    location.reload();
}

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.materialboxed');
    var instances = M.Materialbox.init(elems, {});
});