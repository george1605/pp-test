class HashMapFunctor<T, K>(val hashMap: HashMap<T, K>)
{
    fun map(function: (K) ->(K)): HashMapFunctor<T, K>
    {
        var result = HashMap<T, K>()
        for((key, value) in hashMap){
            result[key] = function(value)
        }
        return HashMapFunctor(result)
    }
}
