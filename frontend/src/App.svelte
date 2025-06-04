<script>
  import { onMount } from 'svelte';
  let episodes = [];
  let selected = null;
  let playbackRate = 1;
  let translation = '';
  let scriptSentences = [];
  let translationSentences = [];
  let highlight = -1;

  onMount(async () => {
    const res = await fetch('/episodes');
    episodes = await res.json();
  });

  const selectEpisode = async (ep) => {
    selected = ep;
    translation = '';
    scriptSentences = ep.script ? ep.script.split(/\u3002/) : [];
    highlight = -1;
    if (ep.script) {
      const res = await fetch('/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: ep.script })
      });
      const data = await res.json();
      translation = data.text;
      translationSentences = translation.split('.');
    }
  };

  const handleTime = (e) => {
    if (!selected || scriptSentences.length === 0) return;
    const ratio = e.target.currentTime / selected.length;
    highlight = Math.floor(ratio * scriptSentences.length);
  };
</script>

<main class="p-4 font-sans">
  <h1 class="text-2xl font-bold mb-4">📻 Kiko Episodes</h1>
  <ul class="space-y-2">
    {#each episodes as ep}
      <li
        class="border p-2 rounded cursor-pointer hover:bg-gray-50 {selected && selected.id === ep.id ? 'bg-gray-100' : ''}"
        on:click={() => selectEpisode(ep)}
      >
        <span class="font-semibold">{ep.title}</span>
        <span class="text-sm text-gray-600">({ep.length}s)</span>
      </li>
    {/each}
  </ul>

  {#if selected}
    <div class="mt-6">
      <h2 class="text-xl font-semibold">{selected.title}</h2>
      <p class="text-gray-700">Length: {selected.length} sec</p>
      <audio bind:playbackRate={playbackRate} on:timeupdate={handleTime} controls class="mt-2 w-full">
        <source src={selected.audio_url} type="audio/mpeg" />
      </audio>
      <label class="block mt-2 text-sm">
        Speed:
        <select bind:value={playbackRate} class="border ml-2 p-1">
          <option value="0.5">0.5x</option>
          <option value="1">1x</option>
          <option value="1.5">1.5x</option>
          <option value="2">2x</option>
        </select>
      </label>
      <div class="mt-4 grid grid-cols-2 gap-4 text-lg leading-relaxed">
        <div>
          {#each scriptSentences as s, i}
            <span class={i === highlight ? 'bg-yellow-200' : ''}>{s}。</span>
          {/each}
        </div>
        <div class="text-gray-700">
          {#each translationSentences as t, i}
            <span class={i === highlight ? 'bg-yellow-200' : ''}>{t}.</span>
          {/each}
        </div>
      </div>
    </div>
  {/if}
</main>

<style>
  main { max-width: 600px; margin: auto; }
</style>
