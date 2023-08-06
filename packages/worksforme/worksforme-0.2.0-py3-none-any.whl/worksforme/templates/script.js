/* boiler plate javascript
 */
var fn = {};

(function(){
let search_timer = null;
let sets = {};
let trash_icon = `<svg width="12" height="12" version="1.1" viewBox="0 0 3.175 3.175" xmlns="http://www.w3.org/2000/svg"><path d="m1.1906 1.2579v1.1896q0 0.03014-0.01809 0.05024-0.01808 0.01808-0.04823 0.01808h-0.13263q-0.03014 0-0.04823-0.01808-0.01809-0.0201-0.01809-0.05024v-1.1896q0-0.03014 0.01809-0.04823 0.01808-0.0201 0.04823-0.0201h0.13263q0.03014 0 0.04823 0.0201 0.01809 0.01808 0.01809 0.04823zm0.53051 0v1.1896q0 0.03014-0.0201 0.05024-0.01808 0.01808-0.04823 0.01808h-0.13062q-0.03014 0-0.05024-0.01808-0.01808-0.0201-0.01808-0.05024v-1.1896q0-0.03014 0.01808-0.04823 0.02009-0.0201 0.05024-0.0201h0.13062q0.03014 0 0.04823 0.0201 0.0201 0.01808 0.0201 0.04823zm0.5285 0v1.1896q0 0.03014-0.01808 0.05024-0.01808 0.01808-0.04823 0.01808h-0.13263q-0.02814 0-0.04823-0.01808-0.01808-0.0201-0.01808-0.05024v-1.1896q0-0.03014 0.01808-0.04823 0.0201-0.0201 0.04823-0.0201h0.13263q0.03014 0 0.04823 0.0201 0.01808 0.01808 0.01808 0.04823zm0.26525 1.4951v-1.9593h-1.8528v1.9593q0 0.04622 0.01407 0.08641 0.01406 0.03818 0.02813 0.05627 0.01608 0.01608 0.0221 0.01608h1.7221q6e-3 0 0.0221-0.01608 0.01608-0.01808 0.03014-0.05627 0.01407-0.04019 0.01407-0.08641zm-1.3906-2.2245h0.92638l-0.09847-0.24114q-0.01005-0.0201-0.03617-0.02412h-0.6551q-0.0221 4e-3 -0.03416 0.02412zm1.9191 0.06631v0.13263q0 0.02813-0.01808 0.04823-0.01808 0.01808-0.04622 0.01808h-0.19894v1.9593q0 0.17282-0.09847 0.29741-0.09847 0.12459-0.2331 0.12459h-1.7221q-0.13664 0-0.23511-0.12057-0.09646-0.12057-0.09646-0.29138v-1.9693h-0.19693q-0.02814 0-0.04823-0.01808-0.01808-0.0201-0.01808-0.04823v-0.13263q0-0.02813 0.01808-0.04622 0.02009-0.0201 0.04823-0.0201h0.63902l0.14469-0.34361q0.03215-0.07636 0.11253-0.13062 0.08038-0.05425 0.16277-0.05425h0.66112q0.08239 0 0.16277 0.05425t0.11253 0.13062l0.14468 0.34362h0.64103q0.02814 0 0.04622 0.0201 0.01808 0.01808 0.01808 0.04622z" stroke-width=".10289"/></svg>`;
let remove_icon = `<svg width="12" height="12" version="1.1" viewBox="0 0 3.175 3.175" xmlns="http://www.w3.org/2000/svg"><path d="m3.0417 2.4727q0 0.098351-0.06825 0.1666l-0.33319 0.3352q-0.06825 0.068245-0.1666 0.068245-0.09635 0-0.16459-0.068245l-0.72058-0.72058-0.72058 0.72058q-0.06825 0.068245-0.1666 0.068245-0.09835 0-0.1666-0.068245l-0.33319-0.3352q-0.06825-0.068245-0.06825-0.1666 0-0.096346 0.06825-0.16459l0.72058-0.72058-0.72058-0.72058q-0.06825-0.068245-0.06825-0.1666 0-0.098351 0.06825-0.1666l0.33319-0.33319q0.06825-0.068245 0.1666-0.068245 0.09835 0 0.1666 0.068245l0.72058 0.72058 0.72058-0.72058q0.06825-0.068245 0.16459-0.068245 0.09835 0 0.1666 0.068245l0.33319 0.33319q0.06825 0.068245 0.06825 0.1666 0 0.098354-0.06825 0.1666l-0.72058 0.72058 0.72058 0.72058q0.06825 0.068245 0.06825 0.16459z" stroke-width=".10277"/></svg>`;
let plus_icon = `<svg width="12" height="12" version="1.1" viewBox="0 0 3.175 3.175" xmlns="http://www.w3.org/2000/svg"><path d="m3.0417 1.3888v0.39742q0 0.08229-0.058209 0.1405-0.058208 0.05821-0.1405 0.05821h-0.85907v0.85706q0 0.0843-0.058208 0.14251-0.056201 0.05821-0.1405 0.05821h-0.39542q-0.084302 0-0.14251-0.05821-0.056201-0.05821-0.056201-0.14251v-0.85706h-0.85907q-0.082294 0-0.1405-0.05821-0.058209-0.05821-0.058209-0.1405v-0.39742q0-0.082293 0.058209-0.1405 0.058208-0.058208 0.1405-0.058208h0.85908v-0.85707q0-0.084302 0.056201-0.14251 0.058208-0.058208 0.14251-0.058208h0.39542q0.084302 0 0.1405 0.058208 0.058208 0.058208 0.058208 0.14251v0.85707h0.85907q0.082295 0 0.1405 0.058208 0.058209 0.058208 0.058209 0.1405z" stroke-width=".10277"/></svg>`;
let play_icon = `<svg width="12" height="12" version="1.1" viewBox="0 0 3.175 3.175" xmlns="http://www.w3.org/2000/svg"><path d="m2.8652 1.6457-2.493 1.3833q-0.043092 0.0237-0.075414 0.00646-0.030168-0.017235-0.030168-0.066793v-2.7623q0-0.049558 0.030168-0.066796 0.032322-0.017237 0.075414 0.006462l2.493 1.3833q0.043092 0.0237 0.043092 0.058176 0 0.034474-0.043092 0.058176z" stroke-width=".11032"/></svg>`;
let loop_icon = `<svg width="12" height="12" version="1.1" viewBox="0 0 3.175 3.175" xmlns="http://www.w3.org/2000/svg"><path d="m3.0417 1.5875q0 0.23685-0.074267 0.45965-0.072258 0.22079-0.20674 0.39943-0.13448 0.17864-0.31513 0.31312-0.17864 0.13448-0.40144 0.20875-0.22079 0.074266-0.45563 0.074266-0.32717 0-0.62022-0.13649-0.29305-0.1385-0.49979-0.38739-0.032114-0.046165 0.004015-0.082295l0.25893-0.26093q0.018065-0.018065 0.048173-0.018065 0.03011 0.00401 0.042151 0.022077 0.1405 0.18065 0.34122 0.279 0.20072 0.098352 0.42552 0.098352 0.26093 0 0.48373-0.12846 0.2248-0.13047 0.35527-0.35326 0.13047-0.2248 0.13047-0.48574 0-0.26294-0.13047-0.48574-0.13047-0.2248-0.35527-0.35527-0.2228-0.13047-0.48373-0.13047-0.18667 0-0.35728 0.068244-0.17061 0.066237-0.30308 0.19068l0.26093 0.26294q0.058208 0.056201 0.026094 0.13047-0.012045 0.032115-0.044158 0.054194-0.032115 0.020073-0.068244 0.020073h-0.84904q-0.048173 0-0.084301-0.034122-0.03613-0.03613-0.03613-0.086308v-0.84904q0-0.080287 0.076273-0.1104 0.074266-0.032114 0.13047 0.026094l0.24488 0.24287q0.20273-0.19068 0.46366-0.29506 0.26093-0.10638 0.53993-0.10638 0.29506 0 0.56402 0.11642 0.26896 0.11642 0.46366 0.31111 0.1947 0.1947 0.30911 0.46366 0.11642 0.26896 0.11642 0.56402z" stroke-width=".10277"/></svg>`;

fn.q = function(q, b=null) {
    if ( b === null ) { b = document; }
    return b.querySelector(q);
};

fn.m = function(t, o={}) {
    let e = document.createElement(t);
    for ( let k of Object.keys(o) ) {
        if ( k == 'class' ) {
            e.className = o[k];
        } else if ( k == 'innerText' ) {
            e.innerText = o[k];
        } else if ( k == 'innerHTML' ) {
            e.innerHTML = o[k];
        } else {
            e.setAttribute(k, o[k]);
        }
    }
    return e;
};

fn.title_case = function(text) {
    let result = '';
    let upper_next = true;
    for ( let idx = 0; idx < text.length; idx++ ) {
        let ch = text.substr(idx, 1);

        if ( upper_next ) {
            ch = ch.toLocaleUpperCase();
        }
        result += ch;

        if ( " \t  ".indexOf(ch) >= 0 ) {
            upper_next = true;
        } else {
            upper_next = false;
        }
    }
    return result;
};

load_sounds = function(data) {
    let sounds = data;
    let container = fn.q('#library');
    container.innerHTML = '';

    let sortable = [];
    Object.entries(sounds).forEach(p => {
        let id = p[0];
        let metadata = p[1];
        if ( !('titles' in metadata) || metadata.titles.length === 0 ) {
            metadata['titles'] = ['untitled']
        }
        sortable.push([id, metadata])
    });
    sortable.sort((a, b) => a[1]['titles'][0].toLocaleLowerCase() > b[1]['titles'][0].toLocaleLowerCase());
    for ( let idx = 0; idx < sortable.length; idx+=1 ) {
        let id = sortable[idx][0];
        let metadata = sortable[idx][1];
        let card = fn.m('li', {'class': 'sound card', 'data-soundid': id});
        let btnplay = fn.m('button', {'class': 'once', 'innerHTML': play_icon});
        let btnloop = fn.m('button', {'class': 'loop', 'innerHTML': loop_icon});
        let title = fn.m('h1');
        let titletext = fn.m('span', {'innerText': metadata['titles'][0]});
        let subtitle = fn.m('h2',
                            {'innerText': metadata['titles'].slice(1).concat(metadata['albums']).join(', ')});
        let len = fn.m('div', {'class': 'duration', 'innerText': metadata['length']});
        card.metadata = metadata;
        container.appendChild(card);
        title.appendChild(btnplay);
        title.appendChild(btnloop);
        title.appendChild(titletext);
        card.appendChild(title);
        card.appendChild(subtitle);
        card.appendChild(len);

        btnplay.onclick = function(ev) { start_play(id, metadata, 'once') };
        btnloop.onclick = function(ev) { start_play(id, metadata, 'loop') };
    }
};

load_sets = function(data) {
    sets = data;
    fill_sets();
};

fill_sets = function() {
    let container = fn.q('#sets');
    container.innerHTML = '';

    let sorted = [];
    Object.entries(sets).forEach(p => {
        sorted.push(p[0]);
    });
    sorted.sort();
    for ( let idx = 0; idx < sorted.length; idx+=1 ) {
        let name = sorted[idx];
        let soundset = sets[name];
        let card = fn.m('li', {'class': 'set card'});
        let title = fn.m('h1');
        let titletext = fn.m('span', {'innerText': name});
        let btnload = fn.m('button', {'class': 'load', 'innerHTML': play_icon, 'title': 'Replace stage with this'});
        let btnadd = fn.m('button', {'class': 'add', 'innerHTML': plus_icon, 'title': 'Add to stage'});
        let btndel = fn.m('button', {'class': 'delete', 'innerHTML': trash_icon, 'title': 'Delete set'});

        title.appendChild(btnload);
        title.appendChild(btnadd);
        title.appendChild(titletext);
        title.appendChild(btndel);
        card.appendChild(title);
        container.appendChild(card);

        btndel.onclick = function(ev) {
            delete sets[name];
            save_sets();
            card.parentElement.removeChild(card);
        };

        let add_set = function() {
            for ( let sdx = 0; sdx < soundset.length; sdx += 1 ) {
                let soundid = soundset[sdx]['soundid'];
                let volume = soundset[sdx]['volume'];
                let option = soundset[sdx]['kind'];
                let sound = null;
                for ( let child of fn.q('#library').children ) {
                    if ( child.getAttribute('data-soundid') === soundid ) {
                        sound = child;
                        break;
                    }
                }
                if ( sound === null ) {
                    continue;
                }

                let card = start_play(soundid, sound.metadata, option);
                fn.q('audio', card).volume = volume;
                fn.q('input', card).value = volume*100;
            }
        };

        btnadd.onclick = function(ev) {
            add_set();
        };
        btnload.onclick = function(ev) {
            stop_all_sounds();
            add_set();
        };
    }
};


stop_all_sounds = function() {
    fn.q('#sounds').innerHTML = '';
};

save_as_set = function(ev) {
    let name = fn.q('#set_name').value;
    if ( name.length == 0 ) {
        return;
    }
    let container = fn.q('#sounds');
    let sounds = [];
    for ( let idx = 0; idx < container.children.length; idx += 1 ) {
        let card = container.children[idx];
        let soundid = card.getAttribute('data-soundid');
        let volume = fn.q('audio', card).volume;
        let kind = 'once';
        if ( card.classList.contains('loop') ) { kind = 'loop' }

        sounds.push({'soundid': soundid,
                     'volume': volume,
                     'kind': kind});
    }

    if ( sounds.length > 0 ) {
        sets[name] = sounds;
        save_sets();
        fill_sets();
        fn.q('#set_name').value = '';
    }
};

save_sets = function() {
    fetch('save', {
        'method': 'POST',
        'headers': {'Content-Type': 'application/json'},
        'body': JSON.stringify(sets)
    });
};

start_play = function(soundid, meta, option) {
    let container = fn.q('#sounds');
    let sound = fn.m('div', {'class': 'card player ' + option, 'data-soundid': soundid});
    let audio = fn.m('audio', {});
    if ( option === 'loop' ) { audio.setAttribute('loop', 'loop') }

    audio.innerHTML = '<source src="sound/' + soundid + '">';
    sound.appendChild(audio);

    let title = fn.m('span', {'innerText': meta['titles'][0]});
    sound.appendChild(title);

    let volume = fn.m('input', {'type': 'range', 'min': '0', 'max': '100'});
    sound.appendChild(volume);

    let btnkill = fn.m('button', {'innerHTML': remove_icon, 'title': 'Remove from stage'});
    sound.appendChild(btnkill);
    container.appendChild(sound);

    volume.value = fn.q('#basevolume').value;
    audio.volume = volume.value / 100.0;
    btnkill.onclick = function(ev){ container.removeChild(sound) };
    volume.onchange = function(ev){ audio.volume = (volume.valueAsNumber / 100.0) * stage_volume() };
    volume.onmousemove = function(ev){ if ( ev.buttons === 1 ) { audio.volume = (volume.valueAsNumber / 100.0) * stage_volume() } };
    if ( option === 'once' ) {
        audio.onended = function(ev){ container.removeChild(sound) };
        audio.oncanplaythrough = function(ev){ audio.play() };
    } else {
        if ( fn.q('#delay').checked ) {
            audio.oncanplaythrough = function(ev){
                const duration = ev.target.duration;
                const wait_time = ((duration / 4.0) * Math.random()) * 1000;
                window.setTimeout(function(){ audio.play() }, wait_time);
            }
        } else {
            audio.oncanplaythrough = function(ev){ audio.play() };
        }
    }

    return sound;
};

start_timeout = function(ev) {
    if ( search_timer !== null ) {
        clearTimeout(search_timer);
    }
    search_timer = setTimeout(apply_search, 250);
};


stage_volume = function() {
    return fn.q('#stage_volume').valueAsNumber / 100.0;
};


on_change_stage_volume = function() {
    const st_volume = stage_volume();
    let container = fn.q('#sounds');
    for ( let idx = 0; idx < container.children.length; idx += 1 ) {
        let audio = fn.q('audio', container.children[idx]);
        let volume = fn.q('input[type=range]', container.children[idx]);

        audio.volume = (volume.valueAsNumber / 100.00) * st_volume;
    }
};

apply_search = function() {
    if ( search_timer !== null ) {
        clearTimeout(search_timer);
        search_timer = null;
    }

    let to_hide = [];
    let to_show = [];
    let container = fn.q('#sidebar ul');
    let searchterms = fn.q('#searchbar').value.split(' ');
    for ( let idx = 0; idx < container.children.length; idx+=1 ) {
        let found_all = true;
        let element = container.children[idx];
        for ( let sdx = 0; sdx < searchterms.length; sdx += 1 ) {
            if ( element.metadata['search'].indexOf(searchterms[sdx]) < 0 ) {
                found_all = false;
                break;
            }
        }

        if ( found_all ) {
            to_show.push(element);
        } else {
            to_hide.push(element);
        }
    }

    to_hide.forEach(element => element.classList.add('hide'));
    to_show.forEach(element => element.classList.remove('hide'));
};

window.onload = function() {
    fetch('sounds.json').then(response => response.json()).then(data => load_sounds(data));
    fetch('sets.json').then(response => response.json()).then(data => load_sets(data));
    fn.q('#searchbar').focus();
    fn.q('#searchbar').onkeyup = start_timeout;
    fn.q('#btnsaveset').onclick = save_as_set;
    fn.q('#btnclear').onclick = stop_all_sounds;
    fn.q('#stage_volume').onchange = on_change_stage_volume;
    fn.q('#stage_volume').onmousemove = function(ev){ if ( ev.buttons === 1 ) { on_change_stage_volume() } };
};

})();
