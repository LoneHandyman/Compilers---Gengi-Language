#include "Scanner/kmp.hpp"

std::vector<std::size_t> lex::kmp(std::string source, std::string pattern, std::vector<int32_t> aux) {
	std::vector<std::size_t> locations;
	int64_t idx_src = 0, idx_pattern = 0;

	while((unsigned)idx_src < source.size()) {
		if(pattern[idx_pattern] == source[idx_src]) {
			++idx_pattern;
			++idx_src;
		}

		if((unsigned)idx_pattern == pattern.size()) {
			locations.push_back(idx_src - idx_pattern);
			idx_pattern = aux[idx_pattern - 1];
		}

		if((unsigned)idx_src < source.size() && pattern[idx_pattern] != source[idx_src]) {
			if(idx_pattern)
				idx_pattern = aux[idx_pattern - 1];
			else
				++idx_src;
		}
	}
  return locations;
}

std::vector<int32_t> lex::prefix(std::string pattern) {
  std::vector<int32_t> kmp_table(pattern.size());
	kmp_table[0] = 0;
	int32_t j = 0, i = 1;

	for(std::size_t j = 0, i = 1; i < pattern.size();) {
		if(pattern[i] == pattern[j])
			kmp_table[i++] = ++j;
		else {
			if(j)
				j = kmp_table[j - 1];
			else
				kmp_table[i++] = 0;
		}
	}
  return kmp_table;
}