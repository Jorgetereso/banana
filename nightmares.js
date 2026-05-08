// ============================================================
// BANANA AIRWAYS · NIGHTMARE STORIES
// Real chaos from low-cost airline passengers.
// ============================================================

const STORIES = [
  { title: "Duct-Taped to His Seat in Row 18", category: "drama", airline: "Frontier", source: { label: "NPR", url: "https://www.npr.org/2021/08/04/1024577106/frontier-airlines-passenger-taped-to-seat-after-allegedly-groping-assaulting-cre" }, summary: "A drunk 22-year-old groped two flight attendants, punched a male attendant, and was duct-taped to his seat from Philadelphia to Miami. He'd taken his shirt off in the bathroom first." },
  { title: "Quit by Emergency Slide With Two Beers", category: "crew", airline: "JetBlue", source: { label: "History.com", url: "https://www.history.com/this-day-in-history/august-9/jetblue-flight-attendant-quits-job-via-escape-slide" }, summary: "Flight attendant Steven Slater cursed out a passenger over the PA, grabbed two beers from the cart, popped the emergency slide at the gate, and slid away into instant folk-hero status." },
  { title: "Door Plug Blown Off at 16,000 Feet", category: "mechanical", airline: "Alaska Airlines", source: { label: "Wikipedia", url: "https://en.wikipedia.org/wiki/Alaska_Airlines_Flight_1282" }, summary: "Six minutes after takeoff from Portland, the door plug ripped off the 737 Max 9 because four bolts were missing. Phones and a kid's shirt got sucked into the sky." },
  { title: "Window Bursts, Passenger Sucked Halfway Out", category: "mechanical", airline: "Southwest", source: { label: "Wikipedia", url: "https://en.wikipedia.org/wiki/Southwest_Airlines_Flight_1380" }, summary: "A fan blade snapped, shrapnel shattered a window, and Jennifer Riordan was partially blown out at 32,000 feet. Other passengers pulled her back in; she died of blunt force trauma." },
  { title: "Drunk Brit Tried to Open the Door", category: "drama", airline: "Ryanair", source: { label: "Deccan Chronicle", url: "https://www.deccanchronicle.com/world/ryanair-flight-diverted-after-drunk-passenger-tries-to-open-exit-mid-air-1907419" }, summary: "A heavily intoxicated passenger tried to crank open the emergency exit mid-flight from London to Alicante. Plane diverted to Toulouse; five men arrested." },
  { title: "Cobra in the Cockpit", category: "animal", airline: "Private charter (S Africa)", source: { label: "NPR", url: "https://www.npr.org/2023/04/05/1168206000/snake-on-a-plane-cobra-cockpit-south-africa" }, summary: "Pilot Rudolf Erasmus felt something cold slide under his shirt and saw a Cape cobra coiled under his seat. He emergency-landed at the nearest airport with the snake still onboard." },
  { title: "Smuggled Cobra Bites Reptile-Shop Owner", category: "animal", airline: "EgyptAir", source: { label: "CNN", url: "https://www.cnn.com/2012/12/04/travel/snake-on-a-plane/index.html" }, summary: "A Jordanian reptile-shop owner smuggled an Egyptian cobra in his carry-on. It bit him mid-flight and started slithering under the seats. Emergency landing followed." },
  { title: "The Diarrhea Plane That Turned Around", category: "other", airline: "Delta", source: { label: "CNN", url: "https://www.cnn.com/travel/delta-flight-diarrhea-biohazard" }, summary: "A passenger sprayed diarrhea down the aisle of an Atlanta-to-Barcelona A350. Crew handed the guy wet wipes; he had to clean it himself with business-class blankets. Plane returned to Atlanta as a biohazard incident." },
  { title: "United 976: Karl Lagerfeld Perfume vs. Feces", category: "other", airline: "United", source: { label: "Wikipedia", url: "https://en.wikipedia.org/wiki/United_Airlines_Flight_976" }, summary: "A drunk first-class passenger defecated on a service cart on a Buenos Aires–JFK flight. Crew sprayed Karl Lagerfeld perfume in the aisles to mask the smell. Food service was canceled." },
  { title: "Stowaway Rat Evacuates 140 People", category: "animal", airline: "IndiGo", source: { label: "NewsBreak", url: "https://www.newsbreak.com/the-independent-517119/4248168855295-stowaway-rat-delays-indigo-flight-to-delhi-by-three-hours" }, summary: "A passenger spotted a rat in the cabin on a Kanpur-to-Delhi flight. Everyone deplaned; flight delayed three hours while crews hunted the rodent." },
  { title: "Mosquito Swarm Tortures Cabin", category: "animal", airline: "IndiGo", source: { label: "Free Press Journal", url: "https://www.freepressjournal.in/viral/macchar-aa-gaye-mosquito-menace-in-lucknow-delhi-flight-leaves-indigo-passengers-scratching-and-swatting-video" }, summary: "A swarm of mosquitoes invaded a Lucknow-to-Delhi flight. Passengers spent the entire trip swatting and scratching while crew did nothing." },
  { title: "Cockroaches Crawling the Bulkhead", category: "animal", airline: "Spirit", source: { label: "Simple Flying", url: "https://simpleflying.com/spirit-airlines-passenger-plane-multiple-roaches/" }, summary: "A passenger filmed two big roaches climbing the wall next to her Big Front Seat. Video hit 8M views; Spirit offered a $60 credit." },
  { title: "Bedbugs Falling From the Ceiling", category: "animal", airline: "Turkish / Delta+KLM", source: { label: "Fortune", url: "https://fortune.com/2025/01/02/airline-passengers-who-found-bedbugs-infesting-their-seats-were-allegedly-rebuffed-by-flight-crew/" }, summary: "On an Istanbul-to-SFO flight, passengers reported bedbugs literally falling from the ceiling. A separate KLM/Delta family is suing for $200K after being bitten across the Atlantic." },
  { title: "Scorpion in the Lunch Tray", category: "animal", airline: "United", source: { label: "ABC News", url: "https://abcnews.com/US/passenger-stung-scorpion-united-flight-san-francisco-atlanta/story?id=67580260" }, summary: "A business-class passenger felt something land on his head. A scorpion fell onto his dinner tray, and stung him when he tried to grab it. United offered vouchers." },
  { title: "Scorpion in the Seat Cushion", category: "animal", airline: "Air Transat", source: { label: "CBC", url: "https://www.cbc.ca/news/canada/calgary/scorpion-air-transat-flight-1.5050236" }, summary: "On final approach to Calgary, a student felt a piercing pain on her back. She'd been sharing her seat with a scorpion the entire flight from Toronto." },
  { title: "Live Worm in the Sandwich", category: "food", airline: "IndiGo", source: { label: "India.com", url: "https://www.india.com/viral/live-worm-in-sandwich-woman-passenger-discovers-some-crawling-in-meal-on-indigo-flight-6621995/" }, summary: "A passenger filmed a live worm crawling out of her in-flight sandwich. PIA had a parallel viral incident with an 'enormous worm' in their food." },
  { title: "The Moldy Vegan Sandwich", category: "food", airline: "Virgin Atlantic", source: { label: "Fox News", url: "https://www.foxnews.com/food-drink/vegan-passenger-horrified-airline-served-rotten-sandwich-flight-worst-meal" }, summary: "A vegan flyer was served a sandwich with charred-moldy peppers and limp zucchini on a Cancun-to-London flight. He called it the worst meal of his life." },
  { title: "6-Year-Old Sent to the Wrong State Alone", category: "weird", airline: "Spirit", source: { label: "CNN", url: "https://www.cnn.com/2023/12/24/travel/spirit-airlines-6-year-old-wrong-flight" }, summary: "A gate agent escorted an unaccompanied 6-year-old onto the wrong plane. He landed in Orlando instead of Fort Myers and called his grandma asking why she wasn't there." },
  { title: "Welsh Couple Lands in Lithuania, Not Spain", category: "weird", airline: "Ryanair", source: { label: "LADbible", url: "https://www.ladbible.com/lifestyle/travel/ryanair-couple-lithuania-instead-of-spain-mistake-219949-20240611" }, summary: "A 12-person birthday group bound for Costa Brava had their boarding passes scanned and ended up in Lithuania. No one stopped them." },
  { title: "Off-Duty Pilot Pulls the Engine Fire Handles", category: "crew", airline: "Horizon Air (Alaska)", source: { label: "CBS", url: "https://www.cbsnews.com/sanfrancisco/news/averted-disaster-on-horizon-air-flight-renews-scrutiny-on-mental-health-of-those-in-the-cockpit/" }, summary: "Joseph Emerson, in the jumpseat, said 'I am not OK,' then yanked both engine fire-extinguisher handles. He'd been awake 40 hours and recently taken magic mushrooms. Crew tackled him." },
  { title: "Pilot in Street Clothes Rants About Her Divorce", category: "crew", airline: "United", source: { label: "NBC Bay Area", url: "https://www.nbcbayarea.com/news/local/pilot-san-francisco-austin-rant-divorce-police/41977/" }, summary: "A United pilot grabbed the intercom on a SFO-bound flight and started crying about her divorce and the recent election. She was removed from the plane." },
  { title: "Drunk Captain Arrested in the Cockpit", category: "crew", airline: "Southwest", source: { label: "Aviation A2Z", url: "https://aviationa2z.com/index.php/2025/08/15/southwest-airlines-pilot-arrested-for-being-drunk/" }, summary: "TSA smelled booze on a captain at Savannah. Police pulled him out of the cockpit minutes before pushback. He admitted to '3 beers.' Plane delayed 4 hours." },
  { title: "Naked Stripper-Sprinter Tries the Cockpit Door", category: "drama", airline: "Southwest", source: { label: "KHOU", url: "https://www.khou.com/article/news/local/caught-on-camera-southwest-passenger-forces-flight-to-return-to-gate-at-hobby-after-stripping-naked-and-causing-disturbance/285-0d3603f0-6c2e-4564-86f5-1f9a5093fbaa" }, summary: "A woman stripped fully naked and ran banging on the cockpit door on a Houston-to-Phoenix flight. Plane returned to gate; she was carted off for psych evaluation." },
  { title: "9 Jack-and-Cokes Aisle Urination", category: "drama", airline: "American", source: { label: "View From The Wing", url: "https://viewfromthewing.com/nightmare-flight-american-airlines-first-class-passenger-caught-urinating-and-flicking-the-bean-after-downing-9-jack-cokes/" }, summary: "A first-class passenger downed nine Jack-and-Cokes, exposed himself, and urinated in the aisle. Flight diverted to Buffalo; he was charged with indecent exposure." },
  { title: "Hen-Party vs. Drunk Man Brawl", category: "drama", airline: "Ryanair", source: { label: "Free Online Library", url: "https://www.thefreelibrary.com/Ryanair+flight+diverted+as+fight+breaks+out+after+'drunk+man+pestered...-a0574215956" }, summary: "A drunk man harassed a hen party until two men started 'trading punches.' Malaga-bound flight forced to land in Madrid." },
  { title: "Boston Brawl (Spirit's Last Days)", category: "drama", airline: "Spirit", source: { label: "Fox News", url: "https://www.foxnews.com/us/spirit-airlines-passengers-brawl-onboard-plane-flight-attendant-attempts-intervene-throwing-down.amp" }, summary: "Two men brawled in the aisle right after touchdown in Boston. Flight attendant on PA: 'If you're not part of that fight, please get off the airplane!'" },
  { title: "22-Hour Delay With Two Chocolate Bars", category: "weather", airline: "Wizz Air", source: { label: "Weston Mercury", url: "https://www.thewestonmercury.co.uk/news/24949114.wizz-air-apology-passenger-panic-attack-delay/" }, summary: "A Luton-to-Warsaw flight was delayed 22 hours by wind. Passengers were given exactly two chocolate bars (a Balaton Bumm and a marzipan stollen) to survive on. One had a panic attack." },
  { title: "Stranded 48 Hours in Frozen Newfoundland", category: "weather", airline: "British Airways", source: { label: "Travel and Tour World", url: "https://www.travelandtourworld.com/news/article/emergency-flight-diversion-strands-hundreds-on-remote-island-in-freezing-weather-prompting-faa-support-and-passenger-care-challenges-on-canadian-arctic-diversion-amid-aviation-safety-and-response-pro/" }, summary: "A medical-emergency diversion to Gander turned into a 48-hour ordeal at -8°C. Checked bags (including winter coats and meds) were locked away the whole time." },
  { title: "Fuel Fumes & Engine-Restart Tarmac Hell", category: "mechanical", airline: "Wizz Air", source: { label: "Medium", url: "https://medium.com/@blackperljoe/wizz-airs-engine-meltdown-what-s-really-going-on-a49044b645ef" }, summary: "Passengers on a Dortmund-Budapest flight were stuck on the tarmac for 3 hours while engineers repeatedly restarted the engines and jet fuel fumes filled the cabin. About 20% of Wizz's fleet was grounded by engine issues." },
  { title: "Cabin Filled With Smoke, Slides Deployed", category: "mechanical", airline: "Allegiant", source: { label: "Tampa Bay Times", url: "https://www.tampabay.com/news/business/airlines/allegiant-flight-makes-emergency-landing-in-california-after-smoke-fills/2338813/" }, summary: "Allegiant Flight 864 to Hagerstown filled with smoke 8 minutes after takeoff; 141 passengers scrambled down emergency slides. Pilot was fired six weeks later." },
  { title: "Hailstorm Smashes the Nose Cone", category: "weather", airline: "Volaris", source: { label: "AirLive", url: "https://airlive.net/emergency/2023/05/16/a-volaris-airbus-a320-has-been-damaged-during-hailstorm/" }, summary: "A Tijuana-to-Monterrey A320 flew through a hailstorm. The nose radome and windscreens were destroyed; aircraft grounded for repairs after diverting to Torreon." },
  { title: "Hailstorm Punches a Hole in the Nose", category: "weather", airline: "Delta", source: { label: "CNN", url: "https://www.cnn.com/2025/10/03/travel/delta-italy-hail-report" }, summary: "Delta dispatchers ignored weather data and sent a plane into Italian hail. A 30-inch hole opened in the nose, the wings dented, the windshield cracked. Diverted to Rome." },
  { title: "Pilot Sucked Halfway Out the Cockpit Window", category: "mechanical", airline: "Sichuan Airlines", source: { label: "Time", url: "https://time.com/5277625/sichuan-airlines-airbus-a319-windshield-shatters/" }, summary: "At 32,000 feet the cockpit windshield exploded outward. The co-pilot was sucked halfway through the hole; the captain flew the plane back manually with a frozen face and ringing ears." },
  { title: "Plane Skids Off Runway, Splits in Three", category: "mechanical", airline: "Pegasus", source: { label: "Wikipedia", url: "https://en.wikipedia.org/wiki/Pegasus_Airlines_Flight_2193" }, summary: "Pegasus 2193 landed long at Sabiha Gokcen, skidded off, dropped 100+ ft down an embankment, and broke into three pieces with the nose nearly sheared off. Three killed, 179 injured." },
  { title: "$3M of Cocaine in the Crew Bag", category: "crew", airline: "JetBlue", source: { label: "NBC LA", url: "https://www.nbclosangeles.com/news/jetblue-airways-plane-flight-attendant-sentence-lax-drug-cocaine-smuggle-luggage/42485/" }, summary: "A flight attendant abandoned a carry-on stuffed with 60 lbs of cocaine at LAX security and ran. She'd been using crew privileges to skip screening on ~10 trips." },
  { title: "Flight Attendant Dances Naked on Coke", category: "crew", airline: "British Airways", source: { label: "View From The Wing", url: "https://viewfromthewing.com/stripped-naked-and-dancing-in-business-class-british-airways-flight-attendants-lavatory-cocaine-binge-sparks-meltdown/" }, summary: "A male crew member did cocaine in the lavatory, then returned to business class, stripped naked, and performed a 'wild, drug-induced dance.' Arrested on landing." },
  { title: "Mid-Air Birth, Tied Off With a Shoelace", category: "medical", airline: "Delta", source: { label: "CNN", url: "https://www.cnn.com/2026/04/27/us/baby-born-on-delta-flight" }, summary: "Two paramedics happened to be onboard an Atlanta-to-Portland flight when a passenger went into labor. They borrowed blankets from strangers and tied off the umbilical cord with a shoelace." },
  { title: "Body in Seat 14 Nobody Could Move", category: "medical", airline: "Qatar Airways", source: { label: "NBC News", url: "https://www.nbcnews.com/news/world/couple-forced-sit-dead-body-plane-4-hours-woman-dies-flight-rcna193617" }, summary: "A woman died mid-flight from Australia to Qatar. Crew propped her in the empty seat next to a couple, who shared a row with the corpse for the remaining four hours." },
  { title: "The Missing Corpse", category: "medical", airline: "Turkish Airlines", source: { label: "Yahoo News", url: "https://www.yahoo.com/news/articles/corpse-airline-passenger-died-mid-203039580.html" }, summary: "A passenger died over Greenland on an Istanbul-to-SFO flight. The plane diverted to Chicago — and somewhere between offloading and tracking, the body went unaccounted for." },
  { title: "Teen Tries to Open Door Over a Coughing Kid", category: "drama", airline: "EasyJet", source: { label: "Aviation A2Z", url: "https://aviationa2z.com/index.php/2025/01/01/easyjet-flight-makes-emergency-landing-amid-unruly-passenger/" }, summary: "A 16-year-old got so angry at a 10-year-old girl coughing nearby that he assaulted cabin crew and tried to crank open the aircraft door. Flight diverted to Bari." },
  { title: "Ghost Flight — All Security Called In Sick", category: "crew", airline: "Ryanair", source: { label: "Simple Flying", url: "https://simpleflying.com/ryanair-ghost-flight-192-stranded-security-sick-leave/" }, summary: "192 passengers were stranded after the entire airport security team called in sick. The Ryanair flight was canceled into a ghost." },
  { title: "Speed Tape on the Wing", category: "mechanical", airline: "Spirit", source: { label: "Aviation Pros", url: "https://www.aviationpros.com/aircraft-maintenance-technology/aircraft-technology/commercial-airline/news/53058957/spirit-worker-seen-taping-plane-wing-before-flight-dont-worry-it-wasnt-duct-tape" }, summary: "A Spirit passenger filmed a worker taping silver tape across a wing before pushback. (It's actually FAA-approved aluminum 'speed tape,' but it looks exactly like duct tape and the video went mega-viral.)" },
  { title: "Salmon Bombs the Wing (Bald Eagle)", category: "weird", airline: "Alaska Airlines", source: { label: "YouTube", url: "https://www.youtube.com/watch?v=RD8Ad1vZZ6o" }, summary: "In 1987 over Juneau, a bald eagle dropped a fish that struck an Alaska Airlines 737 on takeoff. The incident became part of Alaska's design lore." },
  { title: "Reclining-Seat Tooth-Breaker", category: "drama", airline: "Unspecified US carrier", source: { label: "TravelHost", url: "https://travelhost.com/airlines/passenger-slams-seat-back-breaks-teens-teeth" }, summary: "A teen kept kicking the seat in front. The adult finally slammed his seat back so hard it recoiled and broke the teen's teeth." },
  { title: "Punch-the-Reclined-Seat Guy", category: "drama", airline: "American", source: { label: "CNN", url: "https://www.cnn.com/2020/02/18/us/plane-passenger-reclined-seat-cnn/index.html" }, summary: "A man punched a woman's reclined seatback nine times. When she complained, the flight attendant rolled her eyes at her and offered the man free rum." },
  { title: "'Nobody Flies' — Gucci Bag Lady Standoff", category: "drama", airline: "AirAsia", source: { label: "The Rakyat Post", url: "https://www.therakyatpost.com/news/malaysia/2026/04/23/watch-nobody-flies-inside-the-airasia-chongqing-kl-standoff-told-by-the-malaysian-passenger-who-watched-it-all/" }, summary: "A Chinese passenger demanded crew speak Mandarin and refused to deplane after her three friends missed boarding. Other passengers sarcastically applauded — 'Very good, you're the most beautiful' — as she was hauled off, an hour late." },
  { title: "Passengers Storm the Tarmac", category: "drama", airline: "Ryanair", source: { label: "GB News", url: "https://www.gbnews.com/news/world/ryanair-passengers-storm-tarmac-plane-french-border-control" }, summary: "After a French border-control mess left people stranded, Ryanair passengers ran out onto the tarmac to physically block their own plane from leaving without them." },
  { title: "Drunk Riot, Flight 650 Miles Off Course", category: "drama", airline: "EasyJet", source: { label: "GB News", url: "https://www.gbnews.com/news/world/easyjet-flight-chaos-drunken-riots" }, summary: "Drunk passengers turned the cabin into 'Wild West chaos' — the flight ended up 650 miles off course because of the disruption." }
];

const CATEGORIES = [
  { key: "mechanical", label: "Mechanical" },
  { key: "drama",      label: "Passenger drama" },
  { key: "animal",     label: "Animals" },
  { key: "food",       label: "Food" },
  { key: "weather",    label: "Weather" },
  { key: "crew",       label: "Crew" },
  { key: "medical",    label: "Medical" },
  { key: "weird",      label: "Weird" },
  { key: "other",      label: "Other" }
];

// ============================================================
// RENDER
// ============================================================
(() => {
  const grid       = document.getElementById('grid');
  const empty      = document.getElementById('empty');
  const chipsHost  = document.getElementById('chips');
  const search     = document.getElementById('search');
  const countEl    = document.getElementById('storyCount');

  if (!grid) return;

  if (countEl) countEl.textContent = String(STORIES.length);

  // Build chips
  const counts = {};
  STORIES.forEach(s => { counts[s.category] = (counts[s.category] || 0) + 1; });
  if (chipsHost) {
    CATEGORIES.forEach(cat => {
      if (!counts[cat.key]) return;
      const btn = document.createElement('button');
      btn.className = 'chip';
      btn.dataset.cat = cat.key;
      btn.innerHTML = `${cat.label}<span class="chip__count">${counts[cat.key]}</span>`;
      chipsHost.appendChild(btn);
    });
    // The "All" chip already exists — update its count
    const allChip = chipsHost.querySelector('.chip--all');
    if (allChip) {
      allChip.innerHTML = `All<span class="chip__count">${STORIES.length}</span>`;
    }
  }

  // Render stories
  let activeCat = 'all';
  let activeQuery = '';

  const escapeHtml = (s) => s.replace(/[&<>"']/g, c => ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c]));

  const matchesQuery = (s, q) => {
    if (!q) return true;
    const haystack = (s.title + ' ' + s.summary + ' ' + s.airline + ' ' + s.category).toLowerCase();
    return haystack.includes(q);
  };

  const render = () => {
    const q = activeQuery.trim().toLowerCase();
    const list = STORIES.filter(s =>
      (activeCat === 'all' || s.category === activeCat) &&
      matchesQuery(s, q)
    );

    if (list.length === 0) {
      grid.innerHTML = '';
      empty.hidden = false;
      return;
    }
    empty.hidden = true;

    grid.innerHTML = list.map(s => `
      <article class="story">
        <div class="story__top">
          <span class="story__cat story__cat--${s.category}">${escapeHtml(s.category)}</span>
          <span class="story__air">${escapeHtml(s.airline)}</span>
        </div>
        <h3 class="story__title">${escapeHtml(s.title)}</h3>
        <p class="story__summary">${escapeHtml(s.summary)}</p>
        <a class="story__src" href="${s.source.url}" target="_blank" rel="noopener">${escapeHtml(s.source.label)}</a>
      </article>
    `).join('');
  };

  // Chip clicks
  if (chipsHost) {
    chipsHost.addEventListener('click', (e) => {
      const chip = e.target.closest('.chip');
      if (!chip) return;
      chipsHost.querySelectorAll('.chip').forEach(c => c.classList.remove('is-active'));
      chip.classList.add('is-active');
      activeCat = chip.dataset.cat;
      render();
    });
  }

  // Search
  if (search) {
    search.addEventListener('input', () => {
      activeQuery = search.value;
      render();
    });
  }

  render();
})();
