<script>
  import { onMount } from 'svelte';
  let episodes = [];
  let selected = null;
  let playbackRate = 1;

  onMount(async () => {
    const res = await fetch('/episodes');
    episodes = await res.json();
  });

  const selectEpisode = (ep) => {
    selected = ep;
  };
</script>

<main class="p-4 font-sans">
  <h1 class="text-2xl font-bold mb-4">📻 Kiko Episodes</h1>
  <ul class="space-y-2">
    {#each episodes as ep}
      <li class="border p-2 rounded cursor-pointer hover:bg-gray-50" on:click={() => selectEpisode(ep)}>
        <span class="font-semibold">{ep.title}</span> <span class="text-sm text-gray-600">({ep.length}s)</span>
      </li>
    {/each}
  </ul>

  {#if selected}
    <div class="mt-6">
      <h2 class="text-xl font-semibold">{selected.title}</h2>
      <p class="text-gray-700">Length: {selected.length} sec</p>
      <audio bind:playbackRate={playbackRate} controls class="mt-2 w-full">
        <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg" />
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
    </div>
  {/if}
</main>

<style>
  main { max-width: 600px; margin: auto; }
</style>
