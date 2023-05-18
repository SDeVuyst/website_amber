document.addEventListener('DOMContentLoaded', function() {

  const QUOTES = new Map();

  QUOTES.set("We meet ourselves time and time again in a thousand disguises on the path of life.", "- Carl Jung");
  QUOTES.set("Wholeness is not achieved by cutting off a portion of one's being, but by integration of the contraries.", "- Carl Jung");
  QUOTES.set("Man cannot remake himself without suffering, for he is both the marble and the sculptor.", "- Alexis Carrell");
  QUOTES.set("You have your way. I have my way. As for the right way, the correct way, and the only way, it does not exist.", "- Friedrich Nietzsche")
  QUOTES.set("Your vision will become clear only when you can look into your own heart. Who looks outside, dreams; who looks inside, awakes", "- Carl Jung")
  
  const quote = getRandomKey(QUOTES);
  document.getElementById("quote").innerHTML = quote;
  document.getElementById("quote_author").innerHTML = QUOTES.get(quote);

}, false);


window.addEventListener("scroll", function () {

    // Voor navbar
    // Voor juiste sectie aan te duiden in display
    var over_mij_offset = document.getElementById("Over_Mij").getBoundingClientRect().top;
    var filosofie_offset = document.getElementById("Mijn_filosofie").getBoundingClientRect().top;
    var aanbod_offset = document.getElementById("Aanbod").getBoundingClientRect().top;
    var sticky_trigger_element = document.getElementById("main-text").getBoundingClientRect().top;

    var over_mij_header = document.getElementById("over_mij_header");
    var filosofie_header = document.getElementById("mijn_filosofie_header");
    var aanbod_header = document.getElementById("aanbod_header");
    
    let desktop_header = document.getElementById("desktopheader");

    if ( aanbod_offset < 25 ) {
      desktop_header.classList.add("sticky");
      addViewing([aanbod_header])
      removeViewing([filosofie_header, over_mij_header])

    } else if ( filosofie_offset < 25 ) {
      desktop_header.classList.add("sticky");
      addViewing([filosofie_header])
      removeViewing([over_mij_header, aanbod_header])

    } else if ( over_mij_offset < 25 ) {
      desktop_header.classList.add("sticky");
      addViewing([over_mij_header])
      removeViewing([filosofie_header, aanbod_header])
  
    } else if ( sticky_trigger_element < 25 ) {
      desktop_header.classList.add("sticky");

    } else {
      removeViewing([over_mij_header, filosofie_header, aanbod_header])
      desktop_header.classList.remove("sticky");

    }
  });

function toggleMobileMenu(menu) {
    menu.classList.toggle('open');
}

function mobileHeaderClicked() {
  document.getElementById("toggle1").checked = false;
}

function addViewing(objects) {
  for (i=0; i<objects.length; i++) {
    objects[i].classList.add("viewing");
  }
}

function removeViewing(objects) {
  for (i=0; i<objects.length; i++) {
    objects[i].classList.remove("viewing");
  }
}

//https://stackoverflow.com/questions/42739256/how-get-random-item-from-es6-map-or-set
// returns random key from Set or Map
function getRandomKey(collection) {
  let keys = Array.from(collection.keys());
  return keys[Math.floor(Math.random() * keys.length)];
}

// Update ico on dark mode / light mode
lightSchemeIcon = document.querySelector('link#light-scheme-icon');
darkSchemeIcon = document.querySelector('link#dark-scheme-icon');

function onUpdate() {
  if (matcher.matches) {
    lightSchemeIcon.remove();
    document.head.append(darkSchemeIcon);
    console.log("adding dark theme icon")
  } else {
    document.head.append(lightSchemeIcon);
    darkSchemeIcon.remove();
    console.log("adding light theme icon")
  }
}

matcher = window.matchMedia('(prefers-color-scheme: dark)');
matcher.addListener(onUpdate);
onUpdate();