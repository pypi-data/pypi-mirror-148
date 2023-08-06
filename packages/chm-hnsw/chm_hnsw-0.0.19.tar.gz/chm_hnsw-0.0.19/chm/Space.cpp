#include <algorithm>
#include <cmath>
#include "euclideanDistance.hpp"
#include "innerProduct.hpp"
#include "Space.hpp"

namespace chm {
	float Space::getNorm(const float* const data) const {
		auto res = 0.f;

		for(size_t i = 0; i < this->dim; i++)
			res += data[i] * data[i];

		return 1.f / (sqrtf(res) + 1e-30f);
	}

	void Space::normalizeData(const float* const data, float* const res) const {
		const auto norm = this->getNorm(data);

		for(size_t i = 0; i < this->dim; i++)
			res[i] = data[i] * norm;
	}

	uint Space::getCount() const {
		return this->count;
	}

	const float* const Space::getData(const uint id) const {
		return this->data.data() + id * this->dim;
	}

	float Space::getDistance(const uint aID, const uint bID) const {
		return this->getDistance(this->getData(aID), this->getData(bID));
	}

	float Space::getDistance(const float* const a, const float* const b) const {
		return this->distInfo.funcInfo.f(
			a, b, this->dim, this->dim4, this->dim16, this->distInfo.dimLeft
		);
	}

	float Space::getDistance(const float* const aData, const uint bID) const {
		return this->getDistance(aData, this->getData(bID));
	}

	std::string Space::getDistanceName() const {
		return this->distInfo.funcInfo.name;
	}

	const float* const Space::getNormalizedQuery(const float* const data) {
		if(this->normalize) {
			this->normalizeData(data, this->query.data());
			return this->query.data();
		}

		return data;
	}

	bool Space::isEmpty() const {
		return !this->count;
	}

	void Space::prefetch(const uint id) const {
		#if defined(SIMD_CAPABLE)
			_mm_prefetch(reinterpret_cast<const char*>(this->getData(id)), _MM_HINT_T0);
		#endif
	}

	void Space::push(const float* const data, const uint count) {
		if(this->normalize) {
			const size_t prevCount(this->count);

			for(uint i = 0; i < count; i++)
				this->normalizeData(data + i * this->dim, this->data.data() + (prevCount + i) * this->dim);
		}
		else
			std::copy(data, data + count * this->dim, this->data.data() + this->count * this->dim);

		this->count += count;
	}

	Space::Space(const size_t dim, const SpaceKind kind, const size_t maxCount, const SIMDType simdType)
		: count(0), dim4(dim >> 2 << 2), dim16(dim >> 4 << 4),
		distInfo(
			kind == SpaceKind::EUCLIDEAN
			? getEuclideanInfo(dim, this->dim4, this->dim16, simdType)
			: getInnerProductInfo(dim, this->dim4, this->dim16, simdType)
		),
		normalize(kind == SpaceKind::ANGULAR), dim(dim) {

		if(!this->dim)
			throw std::invalid_argument("Number of dimensions must be greater than 0.");
		if(!maxCount)
			throw std::invalid_argument("Maximum number of elements must be greater than 0.");

		this->data.resize(this->dim * maxCount);

		if(this->normalize)
			this->query.resize(this->dim);
	}
}
