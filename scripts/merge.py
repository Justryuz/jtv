def merge_m3u(files, output_file):
    """
    Merges multiple m3u files into a single file.

    :param files: list of m3u filenames to merge
    :param output_file: the output filename for the merged content
    """
    with open(output_file, 'w') as out_file:
        for m3u_file in files:
            with open(m3u_file, 'r') as in_file:
                # Read and write the content of each file to the output file
                out_file.write(in_file.read())
                out_file.write("\n")  # Add a newline after each file for clarity
    print(f"Merged playlists saved to {output_file}.")

# Example usage after your existing M3U generation code
files_to_merge = ['DewaNonton VOD.m3u','playlist.m3u','mylist.m3u8','1.AstroIPTV.m3u','6.other.m3u8','Playlist6.m3u', '7.hello.m3u8','2.raku.m3u8', '0.tvseries.m3u', 'za.m3u']
output_filename = 'merged_playlist.m3u'
merge_m3u(files_to_merge, output_filename)
