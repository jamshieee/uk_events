document.addEventListener("DOMContentLoaded", async () => {
    console.log("✅ product_details.js loaded");

    const container = document.getElementById("product-detail");
    if (!container) {
        console.error("❌ #product-detail not found");
        return;
    }

    const productId = container.dataset.productId;
    console.log("📦 Product ID:", productId);

    if (!productId) {
        container.innerHTML = "<p class='text-red-600'>Product ID missing</p>";
        return;
    }

    try {
        const response = await fetch(`/api/products/${productId}/`);
        console.log("🌐 API status:", response.status);

        if (!response.ok) {
            container.innerHTML = `<p class="text-red-600">API error (${response.status})</p>`;
            return;
        }

        const product = await response.json();
        console.log("📦 Product data:", product);

        renderProduct(product);

    } catch (error) {
        console.error("❌ Fetch failed:", error);
        container.innerHTML = "<p class='text-red-600'>Failed to load product</p>";
    }
});


// =======================
// CAROUSEL STATE
// =======================
let galleryImages = [];
let currentIndex = 0;


// =======================
// RENDER PRODUCT
// =======================
function renderProduct(product) {

    // Build gallery (main image first)
    galleryImages = [];

    if (product.image) {
        galleryImages.push(product.image);
    }

    if (Array.isArray(product.images)) {
        product.images.forEach(img => {
            if (img && img !== product.image) {
                galleryImages.push(img);
            }
        });
    }

    if (!galleryImages.length) {
        galleryImages = ["https://placehold.co/700x520?text=No+Image"];
    }

    currentIndex = 0;

    // ✅ CURRENT PAGE URL
    const productUrl = `${window.location.origin}${window.location.pathname}`;

    // ✅ WHATSAPP MESSAGE
    const whatsappMessage = encodeURIComponent(
        `Hello,\n\nI am interested in the following product:\n\n` +
        `Product: ${product.name}\n` +
        `Price: ₹ ${product.price}\n\n` +
        `Product Link:\n${productUrl}\n\n` +
        `Please share more details.`
    );

    // ✅ EMAIL BODY
    const emailSubject = encodeURIComponent(`Booking Inquiry - ${product.name}`);
    const emailBody = encodeURIComponent(
        `Hello,\n\n` +
        `I am interested in the following product:\n\n` +
        `Product: ${product.name}\n` +
        `Price: ₹ ${product.price}\n\n` +
        `Product Link:\n${productUrl}\n\n` +
        `Please share more details.\n`
    );

    document.getElementById("product-detail").innerHTML = `
        <!-- LEFT : IMAGE CAROUSEL -->
        <div class="flex flex-col items-center gap-4">

            <div
                id="image-container"
                class="w-full max-w-[700px] h-[520px] flex items-center justify-center bg-white rounded-xl overflow-hidden"
            >
                <img
                    id="main-product-image"
                    src="${galleryImages[0]}"
                    class="w-full h-full object-contain transition-opacity duration-300"
                />
            </div>

            ${galleryImages.length > 1 ? `
                <div class="flex gap-3 overflow-x-auto max-w-[700px] px-2 pb-2">
                    ${galleryImages.map((img, index) => `
                        <img
                            src="${img}"
                            data-index="${index}"
                            class="
                                thumbnail
                                w-20
                                h-20
                                object-contain
                                border
                                rounded-lg
                                cursor-pointer
                                transition
                                ${index === 0 ? 'border-green-600' : 'border-gray-300'}
                            "
                        />
                    `).join("")}
                </div>
            ` : ``}

        </div>

        <!-- RIGHT : DETAILS -->
        <div class="flex flex-col justify-center space-y-4 max-w-xl">

            <h1 class="text-3xl font-bold text-gray-900">
                ${product.name}
            </h1>

            <p class="text-2xl font-semibold text-gray-800">
                ₹ ${product.price}
            </p>

            <p class="text-gray-600 leading-relaxed">
                ${product.description}
            </p>

            <!-- ACTION BUTTONS -->
            <div class="space-y-4 pt-6">

                <!-- WhatsApp -->
                <a
                    href="https://wa.me/919946003511?text=${whatsappMessage}"
                    target="_blank"
                    class="w-full flex items-center justify-center gap-3 border-2 border-green-600 text-black font-semibold py-3 rounded-xl hover:bg-green-50 transition"
                >
                    <svg class="w-5 h-5 text-green-600" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M20.52 3.48A11.94 11.94 0 0012.02 0C5.39 0 0 5.37 0 12c0 2.11.55 4.17 1.6 5.98L0 24l6.17-1.62A11.95 11.94 0 0012.02 24C18.65 24 24 18.63 24 12c0-3.2-1.25-6.21-3.5-8.52z"/>
                    </svg>
                    Book on WhatsApp
                </a>

                <!-- Email -->
                <a
                    href="mailto:Ukafreedh@gmail.com?subject=${emailSubject}&body=${emailBody}"
                    class="w-full flex items-center justify-center gap-3 border-2 border-blue-600 text-black font-semibold py-3 rounded-xl hover:bg-blue-50 transition"
                >
                    <svg class="w-5 h-5 text-blue-600" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M20 4H4a2 2 0 00-2 2v12a2 2 0 002 2h16a2 2 0 002-2V6a2 2 0 00-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                    </svg>
                    Book via Email
                </a>

            </div>

            <p class="text-sm text-gray-500 pt-2">
                *Booking confirmed only after direct contact.
            </p>
        </div>
    `;

    setupThumbnailClicks();
    setupSwipe();
}


// =======================
// THUMBNAIL CLICK
// =======================
function setupThumbnailClicks() {
    document.querySelectorAll(".thumbnail").forEach(thumb => {
        thumb.addEventListener("click", () => {
            setMainImage(Number(thumb.dataset.index));
        });
    });
}


// =======================
// CHANGE MAIN IMAGE
// =======================
function setMainImage(index) {
    if (!galleryImages[index]) return;

    currentIndex = index;
    const mainImg = document.getElementById("main-product-image");

    mainImg.classList.add("opacity-0");

    setTimeout(() => {
        mainImg.src = galleryImages[index];
        mainImg.classList.remove("opacity-0");
    }, 150);

    document.querySelectorAll(".thumbnail").forEach((thumb, i) => {
        thumb.classList.toggle("border-green-600", i === index);
        thumb.classList.toggle("border-gray-300", i !== index);
    });
}


// =======================
// MOBILE SWIPE
// =======================
function setupSwipe() {
    const container = document.getElementById("image-container");
    if (!container || galleryImages.length <= 1) return;

    let startX = 0;

    container.addEventListener("touchstart", e => {
        startX = e.touches[0].clientX;
    });

    container.addEventListener("touchend", e => {
        const diff = startX - e.changedTouches[0].clientX;

        if (Math.abs(diff) < 50) return;

        if (diff > 0 && currentIndex < galleryImages.length - 1) {
            setMainImage(currentIndex + 1);
        } else if (diff < 0 && currentIndex > 0) {
            setMainImage(currentIndex - 1);
        }
    });
}
